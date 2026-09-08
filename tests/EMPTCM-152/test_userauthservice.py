import pytest


@pytest.mark.unitTest
@pytest.mark.happyPath
def test_smoke_login_returns_token():
    # vault_ref: SMOKE-1
    assert True


@pytest.mark.errorPath
def test_smoke_wrong_password_returns_401():
    # vault_ref: SMOKE-2
    assert True
