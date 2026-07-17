"""
LangGraph agent for the AI Chat interaction logger.

Graph shape:

    [entry] -> classify_intent -> (route)
        -> log_interaction_tool   -> respond
        -> search_hcp_tool        -> respond
        -> summarize_tool         -> respond
        -> schedule_followup_tool -> respond
        -> edit_interaction_tool  -> respond
        -> general_chat           -> respond

State is a TypedDict carrying the running message, extracted entities,
and any tool result, so each node can read/write shared state
(conversation memory across turns is kept by the caller via session_id
and replayed into `history`).

If GROQ_API_KEY is not configured, nodes fall back to the local
rule-based extractor in extractor.py so the whole app still runs without
external API access.
"""
import logging
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

from app.core.config import settings
from app.agent import extractor

logger = logging.getLogger(__name__)

_FALLBACK_REPLY = (
    "I can help you log a visit, search for a doctor, summarize notes, "
    "or schedule a follow-up. Try: 'Today I visited Dr Sharma at Apollo "
    "Hospital, discussed diabetes medicines, doctor requested samples, "
    "follow up next Monday.'"
)


class AgentState(TypedDict, total=False):
    message: str
    history: List[Dict[str, str]]
    intent: str
    entities: Dict[str, Any]
    tool_result: Dict[str, Any]
    reply: str


def _get_llm():
    """Return a configured Groq chat model, or None if no API key is set."""
    if not settings.GROQ_API_KEY:
        return None
    try:
        from langchain_groq import ChatGroq

        return ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL, temperature=0.2)
    except Exception:
        # Don't crash the app if the optional Groq integration is misconfigured
        # or the package is missing — fall back to the rule-based path, but make
        # the failure visible instead of swallowing it silently.
        logger.warning(
            "Groq LLM unavailable; falling back to rule-based agent.", exc_info=True
        )
        return None


def classify_intent(state: AgentState) -> AgentState:
    """Detect what the user wants: log, search, summarize, schedule, edit, or general chat."""
    text = state["message"].lower()
    if any(k in text for k in ["find", "search", "look up", "show me dr"]):
        intent = "search_hcp"
    elif any(k in text for k in ["summarize", "summary"]):
        intent = "summarize"
    elif any(k in text for k in ["follow up", "follow-up", "schedule", "remind"]):
        intent = "schedule_followup"
    elif any(k in text for k in ["update", "edit", "change the", "correct"]):
        intent = "edit_interaction"
    elif any(k in text for k in ["visited", "met", "discussed", "meeting", "dr "]):
        intent = "log_interaction"
    else:
        intent = "general_chat"
    state["intent"] = intent
    return state


def log_interaction_tool(state: AgentState) -> AgentState:
    """Tool: extract entities from the message and prepare an interaction payload."""
    entities = extractor.extract_entities(state["message"])
    summary = extractor.summarize(state["message"], entities)
    state["entities"] = entities
    state["tool_result"] = {"action": "log_interaction", "summary": summary, "entities": entities}
    return state


def search_hcp_tool(state: AgentState) -> AgentState:
    """Tool: parse a doctor/hospital name out of a search-style message."""
    entities = extractor.extract_entities(state["message"])
    state["tool_result"] = {"action": "search_hcp", "query": entities.get("doctor") or state["message"]}
    return state


def summarize_tool(state: AgentState) -> AgentState:
    """Tool: summarize the provided text and pull out sentiment/products/key points."""
    entities = extractor.extract_entities(state["message"])
    summary = extractor.summarize(state["message"], entities)
    state["tool_result"] = {"action": "summarize", "summary": summary, "products": entities["products"]}
    return state


def schedule_followup_tool(state: AgentState) -> AgentState:
    """Tool: determine a follow-up date/priority and package a reminder payload."""
    entities = extractor.extract_entities(state["message"])
    state["tool_result"] = {
        "action": "schedule_followup",
        "follow_up_date": entities.get("follow_up_date"),
        "priority": entities.get("priority"),
    }
    return state


def edit_interaction_tool(state: AgentState) -> AgentState:
    """Tool: identify fields the user wants changed on an existing interaction."""
    state["tool_result"] = {"action": "edit_interaction", "raw_request": state["message"]}
    return state


def general_chat(state: AgentState) -> AgentState:
    """Fallback conversational node when no specific intent/tool matches."""
    llm = _get_llm()
    if llm:
        try:
            response = llm.invoke(state["message"])
            state["reply"] = response.content
        except Exception:
            # A transient LLM/network/API error should degrade gracefully to the
            # canned guidance rather than 500 the whole /chat request.
            logger.warning(
                "LLM invocation failed; using fallback reply.", exc_info=True
            )
            state["reply"] = _FALLBACK_REPLY
    else:
        state["reply"] = _FALLBACK_REPLY
    state["tool_result"] = {"action": "general_chat"}
    return state


def respond(state: AgentState) -> AgentState:
    """Compose the final natural-language reply from whichever tool ran."""
    if state.get("reply"):
        return state

    result = state.get("tool_result", {})
    action = result.get("action")

    if action == "log_interaction":
        entities = result.get("entities", {})
        bits = [f"Logged interaction. Summary: {result['summary']}"]
        if entities.get("products"):
            bits.append(f"Products: {', '.join(entities['products'])}.")
        if entities.get("follow_up_date"):
            bits.append("A follow-up has been scheduled.")
        state["reply"] = " ".join(bits)
    elif action == "search_hcp":
        state["reply"] = f"Searching HCP records for '{result['query']}'..."
    elif action == "summarize":
        state["reply"] = f"Summary: {result['summary']}"
    elif action == "schedule_followup":
        state["reply"] = (
            f"Follow-up scheduled for {result.get('follow_up_date') or 'a date to confirm'} "
            f"with {result.get('priority')} priority."
        )
    elif action == "edit_interaction":
        state["reply"] = "Got it — tell me the interaction and the field you'd like to update."
    else:
        state["reply"] = state.get("reply") or "How can I help with your HCP interactions today?"
    return state


def route_intent(state: AgentState) -> str:
    return state["intent"]


def build_graph():
    """Compile the LangGraph state graph for the AI Chat agent."""
    graph = StateGraph(AgentState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("log_interaction", log_interaction_tool)
    graph.add_node("search_hcp", search_hcp_tool)
    graph.add_node("summarize", summarize_tool)
    graph.add_node("schedule_followup", schedule_followup_tool)
    graph.add_node("edit_interaction", edit_interaction_tool)
    graph.add_node("general_chat", general_chat)
    graph.add_node("respond", respond)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "log_interaction": "log_interaction",
            "search_hcp": "search_hcp",
            "summarize": "summarize",
            "schedule_followup": "schedule_followup",
            "edit_interaction": "edit_interaction",
            "general_chat": "general_chat",
        },
    )

    for node in [
        "log_interaction",
        "search_hcp",
        "summarize",
        "schedule_followup",
        "edit_interaction",
        "general_chat",
    ]:
        graph.add_edge(node, "respond")

    graph.add_edge("respond", END)

    return graph.compile()


agent_graph = build_graph()


def run_agent(message: str, history: Optional[List[Dict[str, str]]] = None) -> AgentState:
    """Entry point used by the /chat API route."""
    initial_state: AgentState = {"message": message, "history": history or []}
    return agent_graph.invoke(initial_state)
