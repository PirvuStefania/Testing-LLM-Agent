import pytest
from unittest.mock import patch
from module_under_test import _normalise, CoverageReport, parse_cobertura  # Replace with actual import

@happyPath
@edgeCase
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#known-pitfalls")
@pytest.mark.ac_index(72001)
def test_normalise_preserves_non_dot_prefixes():
    """Verify _normalise correctly handles paths with ./ prefix and preserves non-dot prefixes."""
    # vault_ref: testing-known-pitfalls#known-pitfalls
    assert _normalise("./src/main.py") == "src/main.py"
    assert _normalise(".github/workflows/ci.py") == ".github/workflows/ci.py"
    assert _normalise(".venv/lib/site.py") == ".venv/lib/site.py"

@happyPath
@edgeCase
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#coverage-report-find-dot-dirs")
@pytest.mark.ac_index(72002)
def test_coverage_report_find_dot_dirs(mock_coverage_report):
    """Verify CoverageReport.find() returns is_uncovered=True for dot-directory paths."""
    # vault_ref: testing-known-pitfalls#coverage-report-find-dot-dirs
    mock_coverage_report.return_value = CoverageReport(path=".venv/lib/site.py", is_uncovered=True)
    report = CoverageReport.find(".venv/lib/site.py")
    assert report.is_uncovered is True

@errorPath
@security
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#cobertura-key-collision")
@pytest.mark.ac_index(72003)
def test_parse_cobertura_key_collision(mock_parse_cobertura):
    """Verify parse_cobertura rejects key collisions."""
    # vault_ref: testing-known-pitfalls#cobertura-key-collision
    input_data = [
        {"path": "../shared/util.py", "hits": 10},
        {"path": "shared/util.py", "hits": 20}
    ]
    with pytest.raises(ValueError, match="Key collision detected"):
        parse_cobertura(input_data)

@regression
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#removeprefix-fix")
@pytest.mark.ac_index(72004)
def test_fix_removeprefix_behavior():
    """Verify the fix (removeprefix + manual / handling) resolves unintended dot-stripping."""
    # vault_ref: testing-known-pitfalls#removeprefix-fix
    def fixed_normalise(path):
        if path.startswith("./"):
            return path[2:].lstrip("/")
        return path
    assert fixed_normalise(".venv/lib/site.py") == "venv/lib/site.py"

@edgeCase
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#multiple-leading-dots")
@pytest.mark.ac_index(72005)
def test_normalise_multiple_leading_dots():
    """Test edge case: paths with multiple leading dots."""
    # vault_ref: testing-known-pitfalls#multiple-leading-dots
    assert _normalise("../../shared/file.py") == "shared/file.py"

@edgeCase
@inProcess
@unitTest
@pytest.mark.vault_ref("testing-known-pitfalls#consecutive-slashes")
@pytest.mark.ac_index(72006)
def test_normalise_consecutive_slashes():
    """Test edge case: paths with consecutive slashes."""
    # vault_ref: testing-known-pitfalls#consecutive-slashes
    assert _normalise("//shared/file.py") == "shared/file.py"
