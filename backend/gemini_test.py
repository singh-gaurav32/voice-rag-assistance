import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from faiss_retrieve import retrieve_top_k
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Set GEMINI_API_KEY in your environment.")



client = genai.Client(api_key=api_key)

def build_prompt(query, retrieved_chunks):
    """
    Build a prompt for the LLM with retrieved chunks and the user query.
    Each chunk includes a citation.
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


def ask_llm(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents="Explain how AI works in a few words",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                max_output_tokens=20# Disables thinking
            ),
        )
        print(response.text)
    except Exception as e:
        return f"[ERROR] {e}"
    
def answer_question(query, k=1):
    # Step 1: retrieve top chunks
    top_chunks = retrieve_top_k(query, k=k)
    
    # Step 2: build prompt with context
    prompt = build_prompt(query, top_chunks)
    print("\n--- Prompt ---\n")
    print(prompt)
    # Step 3: generate answer from LLM
    answer = ask_llm(prompt)
    print("\n--- Answer ---\n")
    print(answer)
    return answer

if __name__ == "__main__":
    query = "What is the return policy for defective items?"
    answer = answer_question(query)
