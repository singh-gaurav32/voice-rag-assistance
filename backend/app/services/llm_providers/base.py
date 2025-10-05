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
            doc_nice_name = chunk["doc"].replace("_", " ").replace(".md", "").title()
            context += f"[{chunk['doc']}] (from {doc_nice_name + "document"})\n"

        prompt = f"""
            You are a helpful customer support assistant.

            Use the following context to answer the user question.
            Always mention the source document naturally in your answer.
            Explicitly cite the document start with as per our documtation {doc_nice_name}.

            Context:
            {context}

            User Question: {query}

            Answer:
            """
        return prompt
