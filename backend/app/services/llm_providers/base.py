# app/services/llm_base.py

from abc import ABC, abstractmethod

class LLMBase(ABC):
    """
    Abstract base class for LLM providers.
    Subclasses must implement generate_answer().
    """

    @abstractmethod
    def generate_answer(self, query: str, retrieved_chunks: list, **kwargs) -> str:
        """
        Generate a response from the LLM using query and retrieved chunks.

        Args:
            query: User question
            retrieved_chunks: List of dicts with keys 'doc', 'chunk_id', 'text'
            kwargs: Any additional provider-specific parameters

        Returns:
            Answer string
        """
        pass

    def build_prompt(self, query: str, retrieved_chunks: list) -> str:
        """
        Build a standard prompt including citations for all retrieved chunks.
        """
        context = ""
        for chunk in retrieved_chunks:
            context += f"[{chunk['doc']}] {chunk['text']}\n\n"

        prompt = f"""
            You are a helpful customer support assistant.

            Use the following context to answer the user question.
            Include citations in parentheses if possible.

            Context:
            {context}

            User Question: {query}

            Answer:
            """
        return prompt
