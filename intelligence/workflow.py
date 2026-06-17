from typing import TypedDict
from langgraph.graph import StateGraph, END
from intelligence.agents.incident_analyst import generate_incident_report
from intelligence.agents.recommendation_agent import generate_recommendation

class IntelligenceState(TypedDict):
    alert: dict
    incident_report: dict
    recommendations: dict

def analyst_node(state):
    state["incident_report"] = generate_incident_report(state["alert"])
    return state

def recommendation_node(state):
    state["recommendations"] = generate_recommendation(state["alert"])
    return state

graph = StateGraph(IntelligenceState)

graph.add_node("analyst", analyst_node)
graph.add_node("recommendations", recommendation_node)
graph.set_entry_point("analyst")
graph.add_edge("analyst", "recommendations")
graph.add_edge("recommendations", END)

intelligence_workflow = graph.compile()
