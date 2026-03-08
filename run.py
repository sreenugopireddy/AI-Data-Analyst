"""
run.py — Convenience launcher for the AI Data Analyst app.

Equivalent to: streamlit run app/main.py
Can be run with: python run.py
"""

import subprocess
import sys
import os


def main():
    app_path = os.path.join(os.path.dirname(__file__), "app", "main.py")

    if not os.path.exists(app_path):
        print(f"[ERROR] Could not find app at: {app_path}")
        sys.exit(1)

    print("🚀 Starting AI Data Analyst...")
    print("   Open http://localhost:8501 in your browser\n")

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", app_path],
        check=True,
    )


if __name__ == "__main__":
    main()
