# Tests for the Raptor Chatbot application

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from chatbot.engine import ChatEngine, Session, Message
from chatbot.knowledge import classify_intent, get_response, RESPONSES
from chatbot.app import create_app


# ── Knowledge base tests ────────────────────────────────────────────────────

class TestIntentClassification:
    def test_greeting_intents(self):
        for msg in ["hello", "hi there", "hey!", "Good morning"]:
            assert classify_intent(msg) == "greeting", f"Failed for: {msg}"

    def test_farewell_intents(self):
        for msg in ["bye", "goodbye", "see you later"]:
            assert classify_intent(msg) == "farewell", f"Failed for: {msg}"

    def test_bio_hash_intent(self):
        for msg in ["bio-hash", "Bio-Hash Protocol", "biohash"]:
            assert classify_intent(msg) == "bio_hash"

    def test_bark_intent(self):
        for msg in ["BARK protocol", "behavioral axiom", "identity violation"]:
            assert classify_intent(msg) == "bark"

    def test_inevitability_gate_intent(self):
        for msg in ["inevitability gate", "five-stage", "liquidity threshold"]:
            assert classify_intent(msg) == "inevitability_gate"

    def test_proof_chain_intent(self):
        for msg in ["proof chain", "zero-entropy", "C=0 enforced", "C=0 standard"]:
            assert classify_intent(msg) == "proof_chain"

    def test_shield_overview_intent(self):
        for msg in ["sovereign shield", "what is raptor", "shield overview"]:
            assert classify_intent(msg) == "shield_overview"

    def test_installation_intent(self):
        for msg in ["how to install", "setup", "how to run"]:
            assert classify_intent(msg) == "installation"

    def test_example_intent(self):
        for msg in ["show me an example", "demo", "sample code"]:
            assert classify_intent(msg) == "example"

    def test_help_intent(self):
        for msg in ["help", "what can you do", "options"]:
            assert classify_intent(msg) == "help"

    def test_default_intent(self):
        assert classify_intent("xyzzy random nonsense 12345") == "default"

    def test_metrics_intent(self):
        assert classify_intent("HRL score") == "metrics"
        assert classify_intent("shield health") == "metrics"

    def test_configuration_intent(self):
        assert classify_intent("shield configuration") == "configuration"
        assert classify_intent("configuration parameters") == "configuration"


class TestResponseContent:
    def test_all_intents_have_responses(self):
        """Every intent in the pattern list returns a non-empty response."""
        test_intents = [
            "greeting", "farewell", "help", "bio_hash", "bark",
            "inevitability_gate", "proof_chain", "shield_overview",
            "did", "axiomhive", "installation", "configuration",
            "register_node", "capital_flow", "metrics",
            "collapse_thresholds", "canary_shadow", "lop",
            "capability_lattice", "ugw", "ebpf", "thanks",
            "version", "example", "about_authors", "default",
        ]
        for intent in test_intents:
            response = get_response(intent)
            assert response, f"Empty response for intent: {intent}"
            assert len(response) > 10, f"Response too short for intent: {intent}"

    def test_unknown_intent_returns_default(self):
        response = get_response("totally_unknown_xyz")
        assert response == RESPONSES["default"]

    def test_greeting_response_mentions_sovereign_shield(self):
        response = get_response("greeting")
        assert "Sovereign Shield" in response

    def test_bio_hash_response_contains_code(self):
        response = get_response("bio_hash")
        assert "```" in response  # contains a code block

    def test_example_response_contains_code(self):
        response = get_response("example")
        assert "```python" in response


# ── Chat engine tests ───────────────────────────────────────────────────────

class TestChatEngine:
    def setup_method(self):
        self.engine = ChatEngine()

    def test_create_session(self):
        session = self.engine.create_session()
        assert session.session_id
        assert len(session.messages) == 0

    def test_get_nonexistent_session_returns_none(self):
        result = self.engine.get_session("nonexistent-id")
        assert result is None

    def test_chat_creates_session(self):
        result = self.engine.chat(None, "hello")
        assert "session_id" in result
        assert result["session_id"]
        assert result["response"]
        assert result["intent"] == "greeting"

    def test_chat_continues_existing_session(self):
        result1 = self.engine.chat(None, "hello")
        sid = result1["session_id"]
        result2 = self.engine.chat(sid, "bio-hash protocol")
        assert result2["session_id"] == sid
        assert result2["intent"] == "bio_hash"

    def test_chat_stores_message_history(self):
        result = self.engine.chat(None, "hello")
        sid = result["session_id"]
        self.engine.chat(sid, "bark protocol")
        history = self.engine.get_history(sid)
        assert history is not None
        assert len(history) == 4  # 2 user + 2 assistant messages

    def test_get_history_unknown_session_returns_none(self):
        assert self.engine.get_history("unknown-session") is None

    def test_clear_session(self):
        result = self.engine.chat(None, "hello")
        sid = result["session_id"]
        ok = self.engine.clear_session(sid)
        assert ok is True
        history = self.engine.get_history(sid)
        assert history == []

    def test_clear_unknown_session(self):
        assert self.engine.clear_session("nonexistent") is False

    def test_active_session_count(self):
        assert self.engine.active_session_count == 0
        self.engine.chat(None, "hello")
        assert self.engine.active_session_count == 1
        self.engine.chat(None, "hi")
        assert self.engine.active_session_count == 2

    def test_message_length_preserved(self):
        msg = "Tell me about the Bio-Hash Protocol"
        result = self.engine.chat(None, msg)
        history = self.engine.get_history(result["session_id"])
        user_msgs = [m for m in history if m["role"] == "user"]
        assert user_msgs[0]["content"] == msg

    def test_purge_expired_sessions(self):
        import time
        session = self.engine.create_session()
        # Manually set last_active to very old
        session.last_active = time.time() - 7200  # 2 hours ago
        count = self.engine.purge_expired_sessions()
        assert count == 1
        assert self.engine.active_session_count == 0


# ── Flask API tests ─────────────────────────────────────────────────────────

class TestFlaskApp:
    def setup_method(self):
        app = create_app({"TESTING": True})
        self.client = app.test_client()

    def test_health_endpoint(self):
        resp = self.client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["service"] == "raptor-chatbot"
        assert "active_sessions" in data

    def test_root_returns_html(self):
        resp = self.client.get("/")
        assert resp.status_code == 200
        assert b"Raptor" in resp.data

    def test_chat_endpoint_basic(self):
        resp = self.client.post(
            "/api/chat",
            json={"message": "hello"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "session_id" in data
        assert "response" in data
        assert "intent" in data
        assert data["intent"] == "greeting"

    def test_chat_endpoint_maintains_session(self):
        resp1 = self.client.post("/api/chat", json={"message": "hello"})
        sid = resp1.get_json()["session_id"]
        resp2 = self.client.post(
            "/api/chat", json={"message": "bio-hash", "session_id": sid}
        )
        assert resp2.get_json()["session_id"] == sid

    def test_chat_empty_message_returns_400(self):
        resp = self.client.post("/api/chat", json={"message": ""})
        assert resp.status_code == 400

    def test_chat_missing_message_returns_400(self):
        resp = self.client.post("/api/chat", json={})
        assert resp.status_code == 400

    def test_chat_message_too_long_returns_400(self):
        resp = self.client.post("/api/chat", json={"message": "x" * 2001})
        assert resp.status_code == 400

    def test_history_endpoint(self):
        # Create a session first
        resp = self.client.post("/api/chat", json={"message": "hello"})
        sid = resp.get_json()["session_id"]

        resp2 = self.client.get(f"/api/history?session_id={sid}")
        assert resp2.status_code == 200
        data = resp2.get_json()
        assert data["session_id"] == sid
        assert len(data["messages"]) == 2  # user + assistant

    def test_history_missing_session_id_returns_400(self):
        resp = self.client.get("/api/history")
        assert resp.status_code == 400

    def test_history_unknown_session_returns_404(self):
        resp = self.client.get("/api/history?session_id=nonexistent-id")
        assert resp.status_code == 404

    def test_clear_endpoint(self):
        resp = self.client.post("/api/chat", json={"message": "hello"})
        sid = resp.get_json()["session_id"]

        resp2 = self.client.post("/api/clear", json={"session_id": sid})
        assert resp2.status_code == 200
        assert resp2.get_json()["cleared"] is True

    def test_clear_missing_session_id_returns_400(self):
        resp = self.client.post("/api/clear", json={})
        assert resp.status_code == 400

    def test_clear_unknown_session_returns_404(self):
        resp = self.client.post("/api/clear", json={"session_id": "nonexistent"})
        assert resp.status_code == 404

    def test_various_intents_via_api(self):
        test_cases = [
            ("What is BARK?", "bark"),
            ("inevitability gate stages", "inevitability_gate"),
            ("C=0 proof chain", "proof_chain"),
            ("show me an example", "example"),
            ("how to install", "installation"),
        ]
        for message, expected_intent in test_cases:
            resp = self.client.post("/api/chat", json={"message": message})
            data = resp.get_json()
            assert data["intent"] == expected_intent, (
                f"Message '{message}' → got intent '{data['intent']}', "
                f"expected '{expected_intent}'"
            )
