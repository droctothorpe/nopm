from typing import Optional
import pytest

@pytest.fixture
def markers(request):
    """Fixture to allow inspection of markers after a test is running"""
    markers = [m.name for m in request.node.iter_markers()]
    # If the test is inside a class, you might also want class-level markers
    if request.node.parent:
        markers += [m.name for m in request.node.parent.iter_markers()]
    return markers

class FlagHelper:
    """Helper to simplify addition of flags and simplify marker syntax like `python -m "slow or not slow"`"""
    def __init__(self, flag: str, description: Optional[str] = None):
        self.flag = flag

        if description:
            self.description = description
        else:
            self.description = ""

    def add_option(self, parser):
        parser.addoption(
            f"--{self.flag}",
            action='store_true',
            dest=self.flag,
            default=False,
            help=self.description
        )

    def configure(self, config):
        # Register the marker progamatically (pytest will throw warnings otherwise)
        # Ref: https://docs.pytest.org/en/stable/example/markers.html#adding-a-custom-marker-from-a-plugin
        config.addinivalue_line(
            "markers", f"{self.flag}: {self.description}"
        )

        # Handle parser options
        assert hasattr(config.option, self.flag), f"Options did not contain attribute '{self.flag}' was 'add_option(...)' called?"

        if getattr(config.option, self.flag):
            self._add_markexpr(config, f"not {self.flag} or {self.flag}")
        else:
            self._add_markexpr(config, f"not {self.flag}")

    def _add_markexpr(self, config, markexpr: str, join_op: str = "and"):
        if config.option.markexpr == '':
            config.option.markexpr += f"({markexpr})"
        else:
            config.option.markexpr += f" {join_op} ({markexpr})"

FLAG_OLLAMA = FlagHelper("ollama", "Enable Ollama tests")
FLAG_ANTHROPIC = FlagHelper("anthropic", description="Enable Anthropic tetss")

def pytest_addoption(parser):
    FLAG_OLLAMA.add_option(parser)
    FLAG_ANTHROPIC.add_option(parser)

def pytest_configure(config):
    FLAG_OLLAMA.configure(config)
    FLAG_ANTHROPIC.configure(config)
