from intelligence.llm import get_llm
from intelligence.rag.retriever import retrieve_context

def generate_recommendation(alert):
    """
    Generates mitigation and response recommendations for detected attack
    """
    attack_type = alert["attack_type"]

    context = retrieve_context(f"{attack_type} mitigation and response")

    llm = get_llm()

    prompt = f"""
    You are a cybersecurity response advisor.

    Attack Alert: {alert}
    Retrieved Context: {context}

    Generate:
    1. Immediate Response Actions.
    2. Containment Recommendations.
    3. Recovery Actions.
    4. Long-Term Mitigations

    Keep recommendations practical and SOC-oriented.
    """

    response = llm.invoke(prompt)
    return response.content

