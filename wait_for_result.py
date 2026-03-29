#!/usr/bin/env python3
"""
wait_for_result.py — Local blocking script.

Blocks silently until .gpu_state.json reaches 'completed' or 'failed'.
Only prints the final result line to minimize output.

Exit codes:
  0  — experiment completed successfully (state=completed)
  1  — experiment failed (state=failed)
  2  — timed out waiting (local safety net)
  3  — unexpected error
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = ".gpu_state.json"


def read_state(repo: Path) -> dict | None:
    path = repo / STATE_FILE
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}m{s:02d}s"


def main() -> None:
    parser = argparse.ArgumentParser(description="Block until the remote GPU experiment finishes.")
    parser.add_argument("--repo-dir", default=".", help="Shared repo path (default: .)")
    parser.add_argument("--poll-interval", type=float, default=5.0, help="Poll interval in seconds (default: 5)")
    parser.add_argument("--timeout", type=float, default=1200.0, help="Local safety timeout in seconds (default: 1200)")
    args = parser.parse_args()

    repo = Path(args.repo_dir).resolve()
    start_time = time.monotonic()

    try:
        while True:
            elapsed = time.monotonic() - start_time

            if elapsed > args.timeout:
                print(f"TIMEOUT after {fmt_elapsed(elapsed)}")
                sys.exit(2)

            state_data = read_state(repo)
            if state_data is None:
                time.sleep(args.poll_interval)
                continue

            state_name = state_data.get("state", "unknown")
            commit = state_data.get("commit", "?")

            if state_name == "completed":
                print(f"COMPLETED commit={commit} elapsed={fmt_elapsed(elapsed)}")
                sys.exit(0)
            elif state_name == "failed":
                error = state_data.get("error", "unknown")
                exit_code = state_data.get("exit_code", "?")
                print(f"FAILED commit={commit} error={error} exit_code={exit_code} elapsed={fmt_elapsed(elapsed)}")
                sys.exit(1)

            time.sleep(args.poll_interval)

    except KeyboardInterrupt:
        print(f"Interrupted after {fmt_elapsed(time.monotonic() - start_time)}")
        sys.exit(3)


if __name__ == "__main__":
    main()
