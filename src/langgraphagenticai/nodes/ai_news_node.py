import os
import textwrap
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo  # Windows: pip install tzdata

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

IST = ZoneInfo("Asia/Kolkata")
TIME_RANGE = {"daily": "day", "weekly": "week", "monthly": "month"}
OUTPUT_DIR = Path("AINews")

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a news digest editor. Turn the provided articles into a clean markdown digest.

    Rules:
    - Use ONLY information present in the articles. Never add facts, numbers or links that are not given.
    - Group articles by date, in the order given (already newest first). Use dates exactly as provided; do not convert or guess them.
    - If two articles cover the same story, merge them into one bullet and cite both sources.
    - Each bullet: 1-2 plain sentences (max 35 words) stating what happened and why it matters. No hype or marketing language.
    - End each bullet with the source as a link: ([Source name](URL)). If the URL is missing, write (source unavailable). Never invent a URL.
    - If an article has no date, put it under "### Undated" at the end.
    - If there are no articles, reply exactly: No AI news found.

    Output markdown only, no intro or closing text, in this format:

    ### YYYY-MM-DD
    - Summary. ([Source](URL))
    - Summary. ([Source](URL))
    """)


def _parse_date(raw):
    """Tavily returns ISO or RFC 2822 dates. Returns an IST datetime or None."""
    raw = raw or ""
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST)


class AINewsNode:
    """Nodes read from `state` and return ONLY the keys they update."""

    def __init__(self, llm, tavily_api_key=None):
        key = (tavily_api_key or os.environ.get("TAVILY_API_KEY", "")).strip()
        if not key:
            raise ValueError("Please enter your Tavily API key (or set TAVILY_API_KEY).")
        self.tavily = TavilyClient(api_key=key)
        self.llm = llm

    def fetch_news(self, state: dict) -> dict:
        frequency = state["messages"][-1].content.strip().lower()
        if frequency not in TIME_RANGE:
            raise ValueError(f"Unknown time frame: {frequency!r}")

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news India and globally",
            topic="news",
            time_range=TIME_RANGE[frequency],
            max_results=15,
        )
        return {"frequency": frequency, "news_data": response.get("results", [])}

    def summarize_news(self, state: dict) -> dict:
        news_items = state.get("news_data") or []
        if not news_items:
            return {"summary": "No AI news found."}

        # dedupe by URL, convert dates to IST, newest first (undated last)
        seen, rows = set(), []
        for item in news_items:
            url = item.get("url", "")
            if url and url in seen:
                continue
            seen.add(url)
            rows.append((_parse_date(item.get("published_date")), item))
        rows.sort(key=lambda r: r[0] or datetime.min.replace(tzinfo=IST), reverse=True)

        blocks = []
        for dt, item in rows:
            url = item.get("url", "")
            source = item.get("source") or urlparse(url).netloc.removeprefix("www.")
            date_str = f"{dt:%Y-%m-%d}" if dt else "unknown"
            blocks.append(
                f"Date: {date_str}\n"
                f"Title: {item.get('title', '')}\n"
                f"Source: {source}\n"
                f"URL: {url}\n"
                f"Content: {(item.get('content') or '')[:800]}"
            )

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "Articles (newest first, dates in IST):\n\n{articles}"),
        ])
        response = (prompt | self.llm).invoke({"articles": "\n\n".join(blocks)})
        return {"summary": response.content}

    def save_results(self, state: dict) -> dict:
        OUTPUT_DIR.mkdir(exist_ok=True)
        path = OUTPUT_DIR / f"{state['frequency']}_summary.md"
        # utf-8 explicitly: Windows default (cp1252) crashes on curly quotes / emoji
        path.write_text(
            f"# {state['frequency'].capitalize()} AI News Summary\n\n{state['summary']}\n",
            encoding="utf-8",
        )
        return {"filename": str(path)}
