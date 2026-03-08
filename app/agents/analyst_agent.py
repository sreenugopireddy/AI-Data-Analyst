"""
agents/analyst_agent.py — Orchestrates the full analysis pipeline.

This is the "brain" of the app: it coordinates data loading, statistics,
visualization, and LLM interaction into a single coherent workflow.
"""

from __future__ import annotations

import pandas as pd
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE
from analysis.data_loader import get_column_types
from analysis.statistics import (
    compute_descriptive_stats,
    compute_category_stats,
    build_stats_summary_for_llm,
)
from analysis.visualization import (
    plot_revenue_trend,
    plot_product_performance,
    plot_category_comparison,
    plot_correlation_heatmap,
    plot_distribution,
)
from utils.prompts import build_analyst_prompt


class AnalystAgent:
    """
    High-level agent that wraps the analysis pipeline.

    Usage:
        agent = AnalystAgent(df)
        insights = agent.generate_insights()
        charts   = agent.generate_charts()
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.col_types = get_column_types(df)

        # Validate API key early so we surface a clear error in the UI
        if not GROQ_API_KEY:
            raise EnvironmentError(
                "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
            )
        self._client = Groq(api_key=GROQ_API_KEY)

    # ── Public interface ──────────────────────────────────────────────────────

    def generate_insights(self) -> str:
        """
        Send dataset statistics to the Groq LLM and return the AI analysis text.
        """
        stats_summary = build_stats_summary_for_llm(self.df)
        col_info = self._build_column_info()

        system_prompt, user_message = build_analyst_prompt(
            stats_summary=stats_summary,
            column_info=col_info,
            row_count=len(self.df),
        )

        response = self._client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=GROQ_MAX_TOKENS,
            temperature=GROQ_TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )

        return response.choices[0].message.content

    def generate_charts(self) -> dict[str, object]:
        """
        Produce all relevant charts for this dataset.

        Returns a dict mapping chart_title → Matplotlib Figure (or None if not applicable).
        """
        charts: dict[str, object] = {}

        # Time-series revenue trend
        fig = plot_revenue_trend(self.df)
        if fig:
            charts["📈 Revenue Trend Over Time"] = fig

        # Product / top-entity bar chart
        fig = plot_product_performance(self.df)
        if fig:
            charts["🏆 Product Performance"] = fig

        # Category comparison (bar + donut)
        fig = plot_category_comparison(self.df)
        if fig:
            charts["🗂️ Category Comparison"] = fig

        # Correlation heatmap (only if enough numeric columns)
        fig = plot_correlation_heatmap(self.df)
        if fig:
            charts["🔗 Correlation Heatmap"] = fig

        # Distribution of the most interesting numeric column
        priority = ["revenue", "sales", "amount", "price", "units"]
        dist_col = self._pick_distribution_column(priority)
        if dist_col:
            fig = plot_distribution(self.df, dist_col)
            if fig:
                charts[f"📊 Distribution: {dist_col.title()}"] = fig

        return charts

    def get_descriptive_stats(self) -> pd.DataFrame:
        """Return descriptive statistics table for display."""
        return compute_descriptive_stats(self.df)

    def get_category_stats(self) -> dict[str, pd.DataFrame]:
        """Return value-count tables for categorical columns."""
        return compute_category_stats(self.df)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _build_column_info(self) -> str:
        parts = []
        for dtype, cols in self.col_types.items():
            if cols:
                parts.append(f"{dtype}: {', '.join(cols)}")
        return " | ".join(parts)

    def _pick_distribution_column(self, priority: list[str]) -> str | None:
        """Choose the most business-relevant numeric column for a distribution plot."""
        from analysis.statistics import _find_column
        col = _find_column(self.df, priority)
        if col:
            return col
        return self.col_types["numeric"][0] if self.col_types["numeric"] else None
