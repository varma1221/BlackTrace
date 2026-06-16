from os import getenv
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Returns the shared BlackTrace LLM instance.
    """

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=getenv("GROQ_API_KEY")
    )
