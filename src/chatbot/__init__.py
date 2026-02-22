# Raptor Model Chatbot Application
# Conversational interface for the Sovereign Shield system

"""
Raptor Chatbot - Conversational AI for the Sovereign Shield

Provides a web-based chat interface for interacting with and
learning about the Sovereign Shield infrastructure protection system.

Author: Nicholas Michael Grossi - Capability Architect
System: AxiomHive - Deterministic Truth Engine
"""

__version__ = "1.0.0"
__author__ = "Nicholas Michael Grossi"

from chatbot.engine import ChatEngine
from chatbot.app import create_app

__all__ = ["ChatEngine", "create_app"]
