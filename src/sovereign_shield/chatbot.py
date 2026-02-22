"""
Raptor Model - Chat Bot Interface

A GPT-style conversational chat interface that supports chat interview sessions.
Conversations are maintained as a list of role/content message pairs, mirroring
the standard OpenAI chat-completions format.

The chatbot backend is determined by the following environment variables:

  RAPTOR_API_KEY   – API key for the chat-completions endpoint.
  RAPTOR_API_URL   – Base URL of an OpenAI-compatible API
                     (defaults to https://api.openai.com/v1).
  RAPTOR_MODEL     – Model identifier to request
                     (defaults to "gpt-3.5-turbo").

When no API key is set the bot runs in *echo* mode, which is useful for
development and integration testing without a live backend.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

ROLE_SYSTEM = "system"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

DEFAULT_SYSTEM_PROMPT = (
    "You are Raptor, a helpful AI assistant. "
    "Answer questions clearly and concisely."
)

DEFAULT_API_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo"


@dataclass
class Message:
    """A single message in the conversation."""

    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class ConversationHistory:
    """Ordered list of messages that form the current conversation."""

    messages: List[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def clear(self) -> None:
        self.messages.clear()

    def to_list(self) -> List[Dict[str, str]]:
        return [m.to_dict() for m in self.messages]

    def __len__(self) -> int:
        return len(self.messages)


# ---------------------------------------------------------------------------
# Backend helpers
# ---------------------------------------------------------------------------

def _validate_api_url(url: str) -> None:
    """Raise *ValueError* if *url* is not a safe HTTPS or localhost URL."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    is_localhost = hostname in ("localhost", "127.0.0.1", "::1")
    if parsed.scheme not in ("https", "http") or (
        parsed.scheme == "http" and not is_localhost
    ):
        raise ValueError(
            f"api_url must use HTTPS (or HTTP for localhost), got: {url!r}"
        )


def _call_api(
    messages: List[Dict[str, str]],
    api_key: str,
    api_url: str,
    model: str,
) -> str:
    """Send messages to an OpenAI-compatible chat-completions endpoint."""
    payload = json.dumps(
        {"model": model, "messages": messages}
    ).encode("utf-8")

    _validate_api_url(api_url)
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:  # noqa: S310
            body = json.loads(response.read().decode("utf-8"))
        choices = body.get("choices")
        if not choices:
            raise RuntimeError("API response contained no choices")
        message = choices[0].get("message")
        if not message:
            raise RuntimeError("API response choice missing 'message' field")
        content = message.get("content")
        if content is None:
            raise RuntimeError("API response message missing 'content' field")
        return content
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"API request failed with status {exc.code}: {exc.read().decode('utf-8', errors='replace')}"
        ) from exc


# ---------------------------------------------------------------------------
# Main chatbot class
# ---------------------------------------------------------------------------

class Chatbot:
    """
    GPT-style chatbot with persistent conversation history.

    Usage (programmatic)::

        bot = Chatbot()
        reply = bot.send("What is the capital of France?")
        print(reply)

    Usage (interactive CLI)::

        bot = Chatbot()
        bot.run()
    """

    def __init__(
        self,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.api_key: str = api_key or os.environ.get("RAPTOR_API_KEY", "")
        self.api_url: str = api_url or os.environ.get("RAPTOR_API_URL", DEFAULT_API_URL)
        self.model: str = model or os.environ.get("RAPTOR_MODEL", DEFAULT_MODEL)
        self.history = ConversationHistory()
        self._system_message: Dict[str, str] = Message(ROLE_SYSTEM, system_prompt).to_dict()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def send(self, user_message: str) -> str:
        """
        Send *user_message* and return the assistant reply.

        The reply is automatically appended to :attr:`history`.
        """
        self.history.add(ROLE_USER, user_message)

        messages = [self._system_message] + self.history.to_list()

        if self.api_key:
            reply = _call_api(messages, self.api_key, self.api_url, self.model)
        else:
            reply = self._echo_reply(user_message)

        self.history.add(ROLE_ASSISTANT, reply)
        return reply

    def reset(self) -> None:
        """Clear the conversation history."""
        self.history.clear()

    # ------------------------------------------------------------------
    # Interactive CLI
    # ------------------------------------------------------------------

    def run(self) -> None:
        """
        Start an interactive chat session in the terminal.

        The session ends when the user types ``exit``, ``quit``, or sends
        an EOF signal (Ctrl-D on Unix, Ctrl-Z on Windows).
        """
        self._print_banner()

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if user_input.lower() == "reset":
                self.reset()
                print("Raptor: Conversation reset.\n")
                continue

            try:
                reply = self.send(user_input)
            except RuntimeError as exc:
                print(f"[Error] {exc}\n", file=sys.stderr)
                continue

            print(f"Raptor: {reply}\n")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _echo_reply(self, user_message: str) -> str:
        """Fallback reply used when no API key is configured."""
        turn = len(
            [m for m in self.history.messages if m.role == ROLE_USER]
        )
        return (
            f"(Echo mode – no API key set) You said: \"{user_message}\" "
            f"[turn {turn}]"
        )

    @staticmethod
    def _print_banner() -> None:
        print("=" * 60)
        print("  Raptor Chat  –  type 'exit' or 'quit' to leave,")
        print("  'reset' to start a new conversation.")
        print("=" * 60)
        print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Console-script entry point for ``raptor-chat``."""
    system_prompt = os.environ.get("RAPTOR_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
    bot = Chatbot(system_prompt=system_prompt)
    bot.run()


if __name__ == "__main__":
    main()
