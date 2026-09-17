"""
Wrapper around the local target model (served by Ollama).

This is the "system under test" -- the model whose safety training you're
trying to bypass. Keep this class dumb: it just sends a prompt (or a full
conversation) to Ollama and returns the raw text response. All attack logic
lives in strategies/ and pipeline.py, not here.
"""

from config import OLLAMA_HOST, TARGET_MODEL, TEMPERATURE_TARGET
import requests


class TargetModel:
    def __init__(self, model: str = TARGET_MODEL, host: str = OLLAMA_HOST):
        self.model = model
        self.host = host

    def generate(self, messages: list) -> str:
        """
        messages: list of {"role": "user"|"assistant"|"system", "content": str},
        same shape as the OpenAI/Ollama chat format.

        TODO:
        - POST to f"{self.host}/api/chat" with json body:
          {"model": self.model, "messages": messages, "stream": False,
           "options": {"temperature": TEMPERATURE_TARGET}}
        - Raise a clear error on non-200 responses
        - Return response.json()["message"]["content"]
        """
        url = f"{self.host}/api/chat"
        response = requests.post(url, json={"model": self.model, 
                                        "messages": messages, 
                                        "stream": False, 
                                        "options": {"temperature": TEMPERATURE_TARGET}})
        response.raise_for_status()
        return response.json()["message"]["content"]

    def single_turn(self, prompt: str) -> str:
        """Convenience wrapper for a one-off prompt with no history."""
        return self.generate([{"role": "user", "content": prompt}])
