RECOMMENDATION_PROMPT = """
You are a cybersecurity response advisor.

Attack Alert:
{alert}

Retrieved Context:
{context}

Return ONLY valid JSON:

{{
  "immediate_actions": "",
  "containment": "",
  "recovery": "",
  "long_term_mitigations": ""
}}
"""
