import os
from typing import Optional
import typer

from nopm.figure import Figure
from nopm.models import provider_from_config_path
from nopm.util import Spinner

app = typer.Typer(no_args_is_help=True)

@app.command()
def hello():
    print("Hello Sanity")

@app.command()
def figure(
    model_config_path: str,
    description_file: str,
    output_file: Optional[str] = None
):
    if output_file is None:
        output_file = "nopm_figure.svg"
    with open(description_file) as f:
        description = f.read()
    
    provider = provider_from_config_path(model_config_path)
    f = Figure(provider)

    spinner = Spinner(message="Generating figure")
    spinner.start()
    f.generate(description, output_file)
    spinner.stop()

    print("Generated file at: ", output_file)
    file_name, _ = os.path.splitext(output_file)
    print("To convert to PNG, run: ")
    print(f"sips -s format png -o {file_name}.png {output_file}")

def main():
    app()

# import argparse
# import sys
# import threading
# import time
# from itertools import cycle

# from .report import generate_performance_report


# def build_parser() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser(
#         prog="nopm",
#         description="Automate performance management reports from GitHub activity.",
#     )
#     parser.add_argument(
#         "--gh-user",
#         required=True,
#         help="GitHub username to generate a report for.",
#     )
#     parser.add_argument(
#         "--name",
#         required=True,
#         help="Human-friendly name to use in the report title (e.g. 'Jane Doe').",
#     )
#     parser.add_argument(
#         "--start-date",
#         dest="start_date",
#         help="Optional start date in MM/DD/YYYY format; filters PRs, commits, and involvements.",
#     )
#     parser.add_argument(
#         "--output-dir",
#         default="nopm-output",
#         help="Directory to write the markdown report into (default: nopm-output).",
#     )
#     return parser





# def main(argv: list[str] | None = None) -> int:
#     parser = build_parser()
#     args = parser.parse_args(argv)

#     spinner = Spinner()
#     spinner.start()
#     try:
#         out_path = generate_performance_report(
#             gh_user=args.gh_user,
#             name=args.name,
#             start_date=args.start_date,
#             output_dir=args.output_dir,
#         )
#     finally:
#         spinner.stop()

#     print(f"Report written to {out_path}")
#     return 0


# if __name__ == "__main__":  # pragma: no cover
#     raise SystemExit(main())
