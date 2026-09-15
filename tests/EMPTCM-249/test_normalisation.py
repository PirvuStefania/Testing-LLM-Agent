import pytest
from unittest.mock import patch
from module import _normalise, parse_cobertura, CoverageReport

@pytest.mark.happyPath
@pytest.mark.edgeCase
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(1)
def test_normalise_only_strips_dot_slash():
    """Verify _normalise() removes only ./ prefix, not all leading . or /."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("./src/main.py") == "src/main.py"

@pytest.mark.edgeCase
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(2)
def test_normalise_multiple_dots():
    """Verify paths with multiple leading dots normalize correctly."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("../shared/util.py") == "shared/util.py"
    assert _normalise("././file.py") == "./file.py"

@pytest.mark.edgeCase
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(3)
def test_normalise_absolute_paths():
    """Verify absolute paths normalize correctly."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("/app/src/main.py") == "app/src/main.py"
    assert _normalise("/./app/src/main.py") == "app/src/main.py"

@pytest.mark.errorPath
@pytest.mark.regression
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(4)
def test_parse_cobertura_no_key_collisions():
    """Verify parse_cobertura() does not merge distinct files under normalized keys."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    test_data = {
        "../shared/util.py": {"lines": 10},
        "shared/util.py": {"lines": 20}
    }
    result = parse_cobertura(test_data)
    assert len(result) == 2

@pytest.mark.happyPath
@pytest.mark.edgeCase
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(5)
def test_coverage_report_find_dot_dir():
    """Verify CoverageReport.find() returns non-None for dot-directory files."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    normalized_path = _normalise(".venv/lib/site.py")
    assert CoverageReport.find(normalized_path) is not None

@pytest.mark.regression
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(6)
def test_fix_removeprefix_edge_cases():
    """Verify the fix handles edge cases correctly."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("a/b/c") == "a/b/c"
    assert _normalise("./a/b/c") == "a/b/c"
    assert _normalise("a/./b/c") == "a/b/c"

@pytest.mark.regression
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(6)
def test_fix_removeprefix_multiple_dots():
    """Verify fix handles multiple consecutive dots correctly."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("./././file.py") == "./file.py"
    assert _normalise(".././file.py") == "../file.py"
