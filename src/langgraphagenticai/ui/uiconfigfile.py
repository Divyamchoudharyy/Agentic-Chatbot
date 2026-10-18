from configparser import ConfigParser
from pathlib import Path

_DEFAULT_INI = Path(__file__).with_name("uiconfigfile.ini")


class Config:
    def __init__(self, config_file=_DEFAULT_INI):
        self.config = ConfigParser()
        if not self.config.read(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

    def _list(self, key):
        return [v.strip() for v in self.config["DEFAULT"][key].split(",") if v.strip()]

    def get_llm_options(self):
        return self._list("LLM_OPTIONS")

    def get_usecase_options(self):
        return self._list("USECASE_OPTIONS")

    def get_groq_model_options(self):
        return self._list("GROQ_OPTIONS_MODEL")

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE", "").strip()
