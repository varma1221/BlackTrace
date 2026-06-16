from intelligence.llm import get_llm
from intelligence.rag.retriever import retrieve_context

def generate_incident_report(alert):
    """
    Generates an analyst-style incident report.
    """

    attack_type = alert["attack_type"]
    context = retrieve_context(f"{attack_type} attack profile")

    llm = get_llm()
    prompt = f"""
        You are a cybersecurity incident analyst.

        Attack Alert: {alert}

        Retrieved Cybersecurity Context: {context}

        Generate a professional incident report containing:

        1. Attack Summary
        2. MITRE ATT&CK Mapping
        3. Threat Explanation
        4. Potential Impact
        5. Recommended Investigation Steps
        
        Keep the report concise and SOC-oriented.
        """
    
    response = llm.invoke(prompt)
    return response.content

