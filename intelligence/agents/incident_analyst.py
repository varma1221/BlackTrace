import json
from intelligence.llm import get_llm
from intelligence.rag.retriever import retrieve_context
from intelligence.prompts.incident_analysis_prompt import INCIDENT_ANALYSIS_PROMPT

def generate_incident_report(alert):
    """
    Generates an analyst-style incident report.
    """

    if alert["attack_type"] == "BENIGN":
        return {
            "attack_summary": "Traffic classified as BENIGN",
            "mitre_mapping": "N/A",
            "threat_explanation": "The observed network behavior matches normal traffic patterns.",
            "potential_impact": "None identified.",
            "investigation_steps": "Continue routine monitoring. No containment or remediation required."
        }

        
    attack_type = alert["attack_type"]
    context = retrieve_context(f"{attack_type} attack profile")

    llm = get_llm()
    prompt = INCIDENT_ANALYSIS_PROMPT.format(alert=alert, context=context)
    
    response = llm.invoke(prompt)
    content = response.content.strip()

    # Slice out everything between the outer curly braces
    start = content.find('{')
    end = content.rfind('}')

    if start != -1 and end != -1:
        json_str = content[start : end + 1]
    else:
        json_str = content

    return json.loads(json_str)
