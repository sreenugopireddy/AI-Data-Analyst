"""
utils/prompts.py — Prompt templates for the Groq LLM.

Keeping prompts in one place makes it easy to iterate on them
without touching agent or analysis logic.
"""


def build_analyst_prompt(stats_summary: str, column_info: str, row_count: int) -> str:
    """
    Builds the full system + user prompt sent to the LLM.

    Args:
        stats_summary: Stringified descriptive statistics from pandas.
        column_info:   Column names and their dtypes.
        row_count:     Number of rows in the dataset.

    Returns:
        A formatted prompt string ready for the Groq API.
    """

    system_context = (
        "You are an elite data analyst and business intelligence consultant. "
        "Your job is to examine dataset statistics and deliver sharp, actionable insights "
        "to senior business stakeholders — not data scientists. "
        "Write in clear, confident prose. Avoid jargon. Be specific with numbers. "
        "Structure your response with these sections:\n"
        "1. **Executive Summary** (2–3 sentences on the big picture)\n"
        "2. **Key Trends & Patterns** (bullet points, quantified where possible)\n"
        "3. **Standout Observations** (anything unusual, surprising, or worth investigating)\n"
        "4. **Actionable Recommendations** (3–5 concrete next steps for the business)\n"
        "Keep the total response under 500 words. Be direct and impactful."
    )

    user_message = f"""
Here is the dataset you need to analyse:

**Dataset Overview**
- Total records: {row_count:,}
- Columns: {column_info}

**Descriptive Statistics**
{stats_summary}

Please provide your professional analysis following the structure in your instructions.
Focus on business value — what does this data tell us, and what should we do about it?
"""

    # We return both parts so the agent can construct the messages array correctly
    return system_context, user_message.strip()
