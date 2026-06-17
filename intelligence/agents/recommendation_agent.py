import json
from intelligence.llm import get_llm
from intelligence.rag.retriever import retrieve_context
from intelligence.prompts.recommendation_prompt import RECOMMENDATION_PROMPT

def generate_recommendation(alert):
    """
    Generates mitigation and response recommendations for detected attack
    """

    if alert["attack_type"] == "BENIGN":
        return {
            "immediate_actions": "No action required.",
            "containment": "No containment required.",
            "recovery": "No recovery actions required.",
            "long_term_mitigations": "Maintain existing monitoring and security controls."
        }

        
    attack_type = alert["attack_type"]

    context = retrieve_context(f"{attack_type} mitigation and response")

    llm = get_llm()

    prompt = RECOMMENDATION_PROMPT.format(alert=alert, context=context)
    response = llm.invoke(prompt)
    return json.loads(response.content)
