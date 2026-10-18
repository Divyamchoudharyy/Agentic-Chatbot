# Agentic Chatbot

A basic chatbot built with **LangGraph**, **Groq** and **Streamlit**.

> This is my **first end-to-end Agentic AI project**. It is intentionally small: one graph, one node, one LLM. The goal was to learn how the pieces (UI, LLM, graph, state) fit together before building more complex agents.

## How it works

The LangGraph workflow is a single-node graph:

```
START  ->  chatbot (LLM)  ->  END
```

1. The user picks a Groq model and enters an API key in the Streamlit sidebar.
2. The user's message is added to the graph `State` (a list of messages).
3. The `chatbot` node sends the full message history to the LLM and appends the reply.
4. Streamlit renders the conversation. History is kept in `st.session_state`, so the bot remembers earlier turns within a session.

## Tech stack

- [LangGraph](https://github.com/langchain-ai/langgraph) - graph / state orchestration
- [LangChain](https://github.com/langchain-ai/langchain) + `langchain-groq` - LLM interface
- [Groq](https://groq.com/) - LLM inference
- [Streamlit](https://streamlit.io/) - frontend

## Project structure

```
Agentic-Chatbot/
├── app.py                         # Entry point
├── requirements.txt
└── src/langgraphagenticai/
    ├── main.py                    # Wires UI + LLM + graph together
    ├── LLMs/groqllm.py            # Groq model setup
    ├── graphs/graph_builder.py    # Builds and compiles the LangGraph graph
    ├── nodes/basic_chatbot_node.py# The chatbot node
    ├── states/state.py            # Graph state definition
    └── ui/
        ├── uiconfigfile.ini       # Page title, model options
        ├── uiconfigfile.py        # Config reader
        └── streamlit/
            ├── loadui.py          # Sidebar + controls
            └── display_result.py  # Chat rendering
```

## Getting started

**Prerequisites:** Python 3.10+ and a free [Groq API key](https://console.groq.com/keys).

```bash
git clone https://github.com/Divyamchoudharyy/Agentic-Chatbot.git
cd Agentic-Chatbot

python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Run the command from the project root. Then paste your Groq API key in the sidebar (or set the `GROQ_API_KEY` environment variable) and start chatting.

## Roadmap

- [ ] Web search tool (Tavily) for a tool-using agent
- [ ] Conditional edges / routing between nodes
- [ ] Persistent memory across sessions
- [ ] More LLM providers (OpenAI, Ollama)
- [ ] Pin dependency versions

## What I learned

- Structuring a LangGraph app: state, nodes, edges, compile
- Streamlit reruns the whole script on every input, so chat history must live in `st.session_state`
- Keeping UI, LLM and graph logic in separate modules

## Author

**Divyam Choudhary** - [GitHub](https://github.com/Divyamchoudharyy)
