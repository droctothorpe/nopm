import pytest
@pytest.fixture
def markers(request):
    markers = [m.name for m in request.node.iter_markers()]
    # If the test is inside a class, you might also want class-level markers
    if request.node.parent:
        markers += [m.name for m in request.node.parent.iter_markers()]
    return markers

def pytest_addoption(parser):
    # NOTE: This is so you don't have to use the `-m "slow or not slow"` annoying syntax
    parser.addoption(
        "--cli",
        action='store_true',
        dest="cli",
        default=False,
        help="Test CLI interface"
    )

def pytest_configure(config):
    def _add_markexpr(markexpr: str, join_op: str = "and"):
        if config.option.markexpr == '':
            config.option.markexpr += f"({markexpr})"
        else:
            config.option.markexpr += f" {join_op} ({markexpr})"

    if config.option.cli:
        _add_markexpr("not cli or cli")
    else:
        _add_markexpr("not cli")