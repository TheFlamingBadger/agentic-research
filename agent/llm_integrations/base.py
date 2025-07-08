from abc import ABC, abstractmethod

class APIPlatform(ABC):
    
    @abstractmethod
    def chat(self, prompt:str) -> str:
        def chat(self, prompt: str) -> str:
            """Sends a prompt to the AI and returns the response text."""
            pass