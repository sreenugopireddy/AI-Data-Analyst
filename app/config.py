"""
config.py — Central configuration for the AI Data Analyst app.

All environment variables, model settings, and app-level constants
are defined here so every module imports from a single source of truth.
"""

import os
from dotenv import load_dotenv

# Load .env file if present (for local development)
load_dotenv()

# ── Groq API ──────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "llama-3.3-70b-versatile"     # Fast & capable; swap to mixtral if preferred
GROQ_MAX_TOKENS: int = 1024
GROQ_TEMPERATURE: float = 0.4              # Lower = more factual analyst tone

# ── App metadata ──────────────────────────────────────────────────────────────
APP_TITLE: str = "AI Data Analyst"
APP_ICON: str = "📊"
APP_DESCRIPTION: str = (
    "Upload a CSV dataset and let the AI agent surface insights, "
    "trends, and actionable recommendations — instantly."
)

# ── Visualization ─────────────────────────────────────────────────────────────
CHART_STYLE: str = "seaborn-v0_8-whitegrid"
CHART_PALETTE: list[str] = [
    "#4361EE", "#3A86FF", "#7209B7", "#F72585",
    "#4CC9F0", "#4895EF", "#560BAD", "#B5179E",
]
CHART_DPI: int = 150
FIGURE_SIZE_WIDE: tuple[int, int] = (12, 5)
FIGURE_SIZE_SQUARE: tuple[int, int] = (8, 6)
