# Raptor Chatbot Conversation Engine
# Core conversation logic and session management

"""
The ChatEngine manages conversation sessions and produces responses
by combining intent classification from the knowledge base with
optional live queries against the Sovereign Shield components.

Author: Nicholas Michael Grossi
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from chatbot.knowledge import classify_intent, get_response


@dataclass
class Message:
    """A single chat message."""
    message_id: str
    role: str            # "user" or "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }


@dataclass
class Session:
    """A conversation session with history."""
    session_id: str
    messages: List[Message] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)

    def add_message(self, role: str, content: str) -> Message:
        msg = Message(
            message_id=str(uuid.uuid4()),
            role=role,
            content=content,
        )
        self.messages.append(msg)
        self.last_active = time.time()
        return msg

    def to_dict(self) -> Dict:
        return {
            "session_id": self.session_id,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at,
            "last_active": self.last_active,
        }


class ChatEngine:
    """
    Core chatbot engine for the Raptor Model.

    Manages sessions and generates responses using the knowledge base.
    Sessions are kept in memory (suitable for single-process deployments).
    """

    SESSION_TTL = 3600  # 1 hour idle timeout

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def create_session(self) -> Session:
        """Create and register a new conversation session."""
        session = Session(session_id=str(uuid.uuid4()))
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Return a session by ID, or None if expired / unknown."""
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if time.time() - session.last_active > self.SESSION_TTL:
            del self._sessions[session_id]
            return None
        return session

    def get_or_create_session(self, session_id: Optional[str]) -> Session:
        """Return existing session or create a fresh one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        return self.create_session()

    # ------------------------------------------------------------------
    # Response generation
    # ------------------------------------------------------------------

    def chat(self, session_id: Optional[str], user_message: str) -> Dict:
        """
        Process a user message and return the assistant response.

        Args:
            session_id: Existing session ID (or None to start new)
            user_message: Raw text from the user

        Returns:
            dict with keys: session_id, user_message, response, intent, timestamp
        """
        session = self.get_or_create_session(session_id)

        # Record user message
        session.add_message("user", user_message)

        # Classify intent and generate response
        intent = classify_intent(user_message)
        response_text = get_response(intent)

        # Record assistant response
        session.add_message("assistant", response_text)

        return {
            "session_id": session.session_id,
            "user_message": user_message,
            "response": response_text,
            "intent": intent,
            "timestamp": time.time(),
        }

    def get_history(self, session_id: str) -> Optional[List[Dict]]:
        """Return message history for a session."""
        session = self.get_session(session_id)
        if session is None:
            return None
        return [m.to_dict() for m in session.messages]

    def clear_session(self, session_id: str) -> bool:
        """Clear the history for a session (keeps session alive)."""
        session = self.get_session(session_id)
        if session is None:
            return False
        session.messages = []
        return True

    # ------------------------------------------------------------------
    # Housekeeping
    # ------------------------------------------------------------------

    def purge_expired_sessions(self) -> int:
        """Remove all expired sessions. Returns number removed."""
        now = time.time()
        expired = [
            sid for sid, s in self._sessions.items()
            if now - s.last_active > self.SESSION_TTL
        ]
        for sid in expired:
            del self._sessions[sid]
        return len(expired)

    @property
    def active_session_count(self) -> int:
        return len(self._sessions)
