"""Unit tests for the LangGraph AI-chat agent logic."""
from datetime import datetime

import pytest

from app.agent import graph


class TestClassifyIntent:
    @pytest.mark.parametrize(
        "message,expected",
        [
            ("find Dr Sharma", "search_hcp"),
            ("search for cardiologists", "search_hcp"),
            ("look up the record", "search_hcp"),
            ("show me dr gupta", "search_hcp"),
            ("please summarize my notes", "summarize"),
            ("give me a summary", "summarize"),
            ("schedule a follow up", "schedule_followup"),
            ("set a follow-up", "schedule_followup"),
            ("remind me next week", "schedule_followup"),
            ("update the priority", "edit_interaction"),
            ("edit that entry", "edit_interaction"),
            ("change the notes", "edit_interaction"),
            ("correct the date", "edit_interaction"),
            ("today I visited a doctor", "log_interaction"),
            ("met with the physician", "log_interaction"),
            ("we discussed treatment", "log_interaction"),
            ("had a meeting", "log_interaction"),
            ("dr sharma was helpful", "log_interaction"),
            ("hello there", "general_chat"),
        ],
    )
    def test_intent_routing(self, message, expected):
        state = graph.classify_intent({"message": message})
        assert state["intent"] == expected

    def test_search_takes_precedence_over_log(self):
        # "find" (search) is checked before "met" (log)
        state = graph.classify_intent({"message": "find the doctor I met"})
        assert state["intent"] == "search_hcp"


class TestToolNodes:
    def test_log_interaction_tool(self):
        state = graph.log_interaction_tool({"message": "Met Dr. Sharma, discussed insulin"})
        assert state["tool_result"]["action"] == "log_interaction"
        assert state["entities"]["doctor"] == "Dr. Sharma"
        assert "summary" in state["tool_result"]

    def test_search_hcp_tool_uses_doctor(self):
        state = graph.search_hcp_tool({"message": "find Dr. Gupta"})
        assert state["tool_result"]["action"] == "search_hcp"
        assert state["tool_result"]["query"] == "Dr. Gupta"

    def test_search_hcp_tool_falls_back_to_message(self):
        state = graph.search_hcp_tool({"message": "cardiology department"})
        assert state["tool_result"]["query"] == "cardiology department"

    def test_summarize_tool(self):
        state = graph.summarize_tool({"message": "Discussed diabetes and insulin"})
        assert state["tool_result"]["action"] == "summarize"
        assert "Diabetes" in state["tool_result"]["products"]

    def test_schedule_followup_tool(self):
        state = graph.schedule_followup_tool({"message": "urgent follow up next monday"})
        result = state["tool_result"]
        assert result["action"] == "schedule_followup"
        assert result["priority"] == "high"
        assert datetime.fromisoformat(result["follow_up_date"]).weekday() == 0

    def test_edit_interaction_tool(self):
        state = graph.edit_interaction_tool({"message": "change the notes"})
        assert state["tool_result"] == {
            "action": "edit_interaction",
            "raw_request": "change the notes",
        }

    def test_general_chat_without_llm(self, monkeypatch):
        monkeypatch.setattr(graph, "_get_llm", lambda: None)
        state = graph.general_chat({"message": "hi"})
        assert "log a visit" in state["reply"]
        assert state["tool_result"]["action"] == "general_chat"

    def test_general_chat_with_llm(self, monkeypatch):
        class FakeResponse:
            content = "hello from the model"

        class FakeLLM:
            def invoke(self, message):
                return FakeResponse()

        monkeypatch.setattr(graph, "_get_llm", lambda: FakeLLM())
        state = graph.general_chat({"message": "hi"})
        assert state["reply"] == "hello from the model"


class TestGetLlm:
    def test_returns_none_without_api_key(self, monkeypatch):
        monkeypatch.setattr(graph.settings, "GROQ_API_KEY", "")
        assert graph._get_llm() is None


class TestRespond:
    def test_existing_reply_is_preserved(self):
        state = graph.respond({"reply": "already set", "tool_result": {"action": "search_hcp"}})
        assert state["reply"] == "already set"

    def test_log_interaction_reply(self):
        state = graph.respond(
            {
                "tool_result": {
                    "action": "log_interaction",
                    "summary": "Met with Dr. Sharma",
                    "entities": {"products": ["Insulin"], "follow_up_date": "2026-01-01T00:00:00"},
                }
            }
        )
        assert "Logged interaction" in state["reply"]
        assert "Products: Insulin." in state["reply"]
        assert "follow-up has been scheduled" in state["reply"]

    def test_search_reply(self):
        state = graph.respond({"tool_result": {"action": "search_hcp", "query": "Dr. Gupta"}})
        assert state["reply"] == "Searching HCP records for 'Dr. Gupta'..."

    def test_summarize_reply(self):
        state = graph.respond({"tool_result": {"action": "summarize", "summary": "some notes"}})
        assert state["reply"] == "Summary: some notes"

    def test_schedule_reply_with_date(self):
        state = graph.respond(
            {"tool_result": {"action": "schedule_followup", "follow_up_date": "2026-01-01", "priority": "high"}}
        )
        assert "2026-01-01" in state["reply"]
        assert "high priority" in state["reply"]

    def test_schedule_reply_without_date(self):
        state = graph.respond(
            {"tool_result": {"action": "schedule_followup", "follow_up_date": None, "priority": "medium"}}
        )
        assert "a date to confirm" in state["reply"]

    def test_edit_reply(self):
        state = graph.respond({"tool_result": {"action": "edit_interaction"}})
        assert "field you'd like to update" in state["reply"]

    def test_unknown_action_fallback(self):
        state = graph.respond({"tool_result": {"action": "mystery"}})
        assert "How can I help" in state["reply"]


class TestRouteIntent:
    def test_route_intent_returns_intent(self):
        assert graph.route_intent({"intent": "summarize"}) == "summarize"


class TestRunAgent:
    def test_run_agent_end_to_end_log(self):
        result = graph.run_agent("Today I visited Dr. Sharma at Apollo Hospital, discussed insulin")
        assert result["intent"] == "log_interaction"
        assert "Logged interaction" in result["reply"]

    def test_run_agent_general_chat(self, monkeypatch):
        monkeypatch.setattr(graph, "_get_llm", lambda: None)
        result = graph.run_agent("hello")
        assert result["intent"] == "general_chat"
        assert result["reply"]

    def test_run_agent_defaults_history(self):
        result = graph.run_agent("find Dr. Sharma")
        assert result["intent"] == "search_hcp"
