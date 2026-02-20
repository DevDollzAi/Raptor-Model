#!/usr/bin/env python3
# Raptor Chatbot — Application Entry Point
# Launch with: python chatbot_app.py

"""
Starts the Raptor AI chatbot web application.

Usage:
    python chatbot_app.py [--host HOST] [--port PORT] [--debug]

Environment variables:
    CHATBOT_HOST   Bind host (default: 127.0.0.1)
    CHATBOT_PORT   Bind port (default: 5000)
    CHATBOT_DEBUG  Enable debug mode (default: false)
    SECRET_KEY     Flask secret key (change in production)
"""

import os
import sys
import argparse

# Ensure src/ is on the path so the package is importable from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from chatbot.app import create_app


def parse_args():
    parser = argparse.ArgumentParser(
        description="Raptor AI Chatbot — Sovereign Shield Assistant"
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("CHATBOT_HOST", "127.0.0.1"),
        help="Host to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("CHATBOT_PORT", "5000")),
        help="Port to listen on (default: 5000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.environ.get("CHATBOT_DEBUG", "").lower() in ("1", "true", "yes"),
        help="Enable Flask debug mode",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    app = create_app()

    print("=" * 60)
    print("  ⚔️  Raptor AI — Sovereign Shield Assistant  v1.0.0")
    print("=" * 60)
    print(f"  🌐  Open in browser: http://{args.host}:{args.port}")
    print(f"  🔒  C=0 Proof Chain: ENFORCED")
    print(f"  📡  API endpoints available at /api/*")
    print("=" * 60)
    print("  Press Ctrl+C to stop the server")
    print()

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
