# Raptor Chatbot Flask Application
# Web server and REST API for the chat interface

"""
Flask application providing the web UI and JSON API for the Raptor chatbot.

Routes:
    GET  /              → Serve the chat HTML UI
    POST /api/chat      → Send a message, receive a response
    GET  /api/history   → Retrieve session message history
    POST /api/clear     → Clear session history
    GET  /api/health    → Health check endpoint

Author: Nicholas Michael Grossi
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from chatbot.engine import ChatEngine


def create_app(test_config=None) -> Flask:
    """
    Application factory for the Raptor chatbot.

    Args:
        test_config: Optional dict of config overrides (for testing)

    Returns:
        Configured Flask application
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "raptor-dev-key-change-in-production"),
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    CORS(app)

    # Single shared engine instance per app
    engine = ChatEngine()

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.get("/")
    def index():
        """Serve the main chat interface."""
        return render_template("index.html")

    @app.post("/api/chat")
    def chat():
        """
        Process a chat message.

        Request JSON:
            {
                "message": "your question here",
                "session_id": "optional-existing-session-id"
            }

        Response JSON:
            {
                "session_id": "...",
                "response": "...",
                "intent": "...",
                "timestamp": 1234567890.0
            }
        """
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({"error": "message is required"}), 400
        if len(message) > 2000:
            return jsonify({"error": "message too long (max 2000 characters)"}), 400

        session_id = data.get("session_id")
        result = engine.chat(session_id, message)
        return jsonify(result)

    @app.get("/api/history")
    def history():
        """
        Retrieve message history for a session.

        Query param: session_id
        """
        session_id = request.args.get("session_id", "").strip()
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400

        msgs = engine.get_history(session_id)
        if msgs is None:
            return jsonify({"error": "session not found or expired"}), 404

        return jsonify({"session_id": session_id, "messages": msgs})

    @app.post("/api/clear")
    def clear():
        """
        Clear message history for a session.

        Request JSON: {"session_id": "..."}
        """
        data = request.get_json(silent=True) or {}
        session_id = (data.get("session_id") or "").strip()
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400

        ok = engine.clear_session(session_id)
        if not ok:
            return jsonify({"error": "session not found or expired"}), 404

        return jsonify({"session_id": session_id, "cleared": True})

    @app.get("/api/health")
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "ok",
            "service": "raptor-chatbot",
            "version": "1.0.0",
            "active_sessions": engine.active_session_count,
        })

    return app
