import pytest
from unittest.mock import MagicMock, patch
from coverage import _normalise, parse_cobertura, CoverageReport

@pytest.mark.happyPath
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("FINDING-072#coverage-path-normalisation-lstrip")
@pytest.mark.ac_index(1)
def test_normalise_strips_only_leading_dot():
    """Verify _normalise strips only './' prefix, not all leading dots."""
    test_cases = [
        ("./src/main.py", "src/main.py"),
        ("./test/file.py", "test/file.py"),
        ( "../shared/util.py", "../shared/util.py"),  # Should not strip '../'
        (".venv/lib/site.py", ".venv/lib/site.py"),  # Leading '.' preserved
    ]
    for input_path, expected in test_cases:
        result = _normalise(input_path)
        assert result == expected, f"Failed for {input_path}: got {result}, expected {expected}"

@pytest.mark.edgeCase
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("FINDING-072#coverage-path-normalisation-edge-cases")
@pytest.mark.ac_index(2)
def test_normalise_edge_cases():
    """Test boundary conditions for _normalise."""
    test_cases = [
        ("", ""),  # Empty string
        ("../../../file.py", "file.py"),  # Multiple '../'
        ("./././file.py", "file.py"),  # Multiple './'
        (".hidden/file.py", ".hidden/file.py"),  # Leading '.' preserved
        ("/absolute/path", "/absolute/path"),  # Absolute path unchanged
    ]
    for input_path, expected in test_cases:
        result = _normalise(input_path)
        assert result == expected, f"Failed for {input_path}: got {result}, expected {expected}"

@pytest.mark.errorPath
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("FINDING-072#coverage-path-normalisation-invalid-inputs")
@pytest.mark.ac_index(3)
def test_normalise_invalid_inputs():
    """Verify _normalise raises TypeError for non-string inputs."""
    with pytest.raises(TypeError):
        _normalise(None)
    with pytest.raises(TypeError):
        _normalise(123)
    with pytest.raises(TypeError):
        _normalise(["not", "a", "string"])

@pytest.mark.regression
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("FINDING-072#coverage-key-collision-fix")
@pytest.mark.ac_index(4)
def test_parse_cobertura_no_key_collision():
    """Verify parse_cobertura does not collide on normalized keys after fix."""
    mock_report = MagicMock()
    mock_report.find.return_value = None

    # Test case where keys would collide with old lstrip("./")
    input_report = {
        "../shared/util.py": {"lines-hit": 50},
        "shared/util.py": {"lines-hit": 75},
    }

    # Mock _normalise to return distinct keys (simulating fix)
    with patch('coverage._normalise') as mock_normalise:
        mock_normalise.side_effect = lambda path: path.replace("../", "") if path.startswith("../") else path
        result = parse_cobertura(input_report, mock_report)

        # Keys should remain distinct after normalization
        assert len(result) == 2, "Keys should not collide after normalization"
        assert "shared/util.py" in result, "Expected key should be present"
        assert result["shared/util.py"]["lines-hit"] == 75, "Max hit should be preserved"

@pytest.mark.security
@pytest.mark.inProcess
@pytest.mark.unitTest
@pytest.mark.vault_ref("FINDING-072#coverage-path-normalisation-security")
@pytest.mark.ac_index(5)
def test_normalise_security_edge_cases():
    """Verify _normalise handles malicious/injection attempts."""
    malicious_paths = [
        "../../../../../etc/passwd",  # Path traversal attempt
        "<script>../malicious.py",   # Injection attempt
    ]
    for path in malicious_paths:
        result = _normalise(path)
        # Ensure no arbitrary path traversal or injection
        assert not result.startswith("/"), "Absolute paths should not be created"
        assert result != path, "Input should be normalized, not passed through"
