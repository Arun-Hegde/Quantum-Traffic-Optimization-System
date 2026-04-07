"""
run.py — One-click launcher for the Quantum Traffic Optimization System.

Usage:
    python run.py          # starts both FastAPI + Streamlit
    python run.py --api    # starts FastAPI only
    python run.py --ui     # starts Streamlit only
    python run.py --test   # runs all tests
"""
import subprocess
import sys
import os
import time
import argparse

if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))


def run_tests():
    print("\n" + "=" * 60)
    print("  🧪 Running All Tests")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=BASE,
    )
    return result.returncode


def start_api():
    print("\n🚀 Starting FastAPI server on http://127.0.0.1:8000")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"],
        cwd=BASE,
    )


def start_ui():
    print("🖥️  Starting Streamlit UI on http://localhost:8501")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        cwd=BASE,
    )


def main():
    parser = argparse.ArgumentParser(description="Quantum Traffic Optimizer Launcher")
    parser.add_argument("--api",  action="store_true", help="Start FastAPI only")
    parser.add_argument("--ui",   action="store_true", help="Start Streamlit only")
    parser.add_argument("--test", action="store_true", help="Run all tests")
    args = parser.parse_args()

    print("""
  ╔══════════════════════════════════════════════════╗
  ║  🚦 Quantum Traffic Optimization System v2.0     ║
  ║     Hyderabad Smart City | QAOA + GenAI          ║
  ╚══════════════════════════════════════════════════╝
    """)

    if args.test:
        sys.exit(run_tests())

    procs = []
    if args.api:
        procs.append(start_api())
    elif args.ui:
        procs.append(start_ui())
    else:
        # Default: start both
        api_proc = start_api()
        procs.append(api_proc)
        time.sleep(3)   # give FastAPI a moment to boot
        ui_proc = start_ui()
        procs.append(ui_proc)

    print("\n✅ System running. Press Ctrl+C to stop.\n")
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        print("\n⛔ Shutting down…")
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    main()
