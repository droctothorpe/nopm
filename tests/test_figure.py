import os
from pathlib import Path
import subprocess

import pytest

from nopm.figure import Figure
from nopm.models import provider_from_config_path

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DESCRIPTION_PATH = os.path.join(THIS_DIR, "description_kfp.md")

CONFIG_OPENAI_OLLAMA = os.path.join(THIS_DIR, "openai_ollama.yml")
CONFIG_OLLAMA_CHAT = os.path.join(THIS_DIR, "ollama_chat.yml")
CONFIG_OLLAMA_GENERATE = os.path.join(THIS_DIR, "ollama_generate.yml")

@pytest.mark.parametrize(
    "config_path",
    [
        CONFIG_OPENAI_OLLAMA,
        CONFIG_OLLAMA_CHAT,
        CONFIG_OLLAMA_GENERATE,
    ]
)
def test_generation(tmp_path: Path, markers, config_path: str):
    # Test programmatic generation
    output_path = tmp_path / "generated.svg"
    with open(DESCRIPTION_PATH) as f:
        description = f.read()

    provider = provider_from_config_path(config_path)
    f = Figure(provider)
    f.generate(description, str(output_path))
    assert output_path.exists()

    if "cli" in markers:
        # Test CLI generation
        output_path = tmp_path / "generated_cli.svg"
        _ =subprocess.run(
            [
                "nopm",
                "figure",
                config_path,
                str(DESCRIPTION_PATH),
                "--output-file", str(output_path),
            ],
            check=True
        )
        assert output_path.exists()
