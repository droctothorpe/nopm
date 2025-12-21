import argparse
import sys
import threading
import time
from itertools import cycle

from .report import generate_performance_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nopm",
        description="Automate performance management reports from GitHub activity.",
    )
    parser.add_argument(
        "--gh-user",
        required=True,
        help="GitHub username to generate a report for.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Human-friendly name to use in the report title (e.g. 'Jane Doe').",
    )
    parser.add_argument(
        "--start-date",
        dest="start_date",
        help="Optional start date in MM/DD/YYYY format; filters PRs, commits, and involvements.",
    )
    parser.add_argument(
        "--output-dir",
        default="nopm-output",
        help="Directory to write the markdown report into (default: nopm-output).",
    )
    return parser


class Spinner:
    """Simple terminal spinner shown while work is in progress."""

    def __init__(self, message: str = "Generating report") -> None:
        self._message = message
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        def run() -> None:
            symbols = cycle(["|", "/", "-", "\\"])
            while not self._stop.is_set():
                ch = next(symbols)
                sys.stdout.write(f"\r{self._message} {ch}")
                sys.stdout.flush()
                time.sleep(0.1)
            # Clear line when stopping
            sys.stdout.write("\r" + " " * (len(self._message) + 4) + "\r")
            sys.stdout.flush()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    spinner = Spinner()
    spinner.start()
    try:
        out_path = generate_performance_report(
            gh_user=args.gh_user,
            name=args.name,
            start_date=args.start_date,
            output_dir=args.output_dir,
        )
    finally:
        spinner.stop()

    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
