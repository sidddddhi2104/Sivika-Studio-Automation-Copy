"""Parameterized data for form tests. Contains no real credentials.

Registration data is deliberately limited to values that can NOT create a valid account,
because the tests run against a live site and must not pollute its database."""
import pytest

# Malformed e-mail addresses. Every other field is left empty, so none of these can register.
INVALID_EMAILS = [
    "plainaddress",
    "missing-at-sign.com",
    "@no-local-part.com",
    "user@@double-at.com",
    "user@",
]

# (identity, password) pairs that must NOT log anyone in.
INVALID_LOGINS = [
    pytest.param("qa.invalid.user@example.com", "WrongPassword!1", id="unknown-user-wrong-password"),
    pytest.param("", "SomePassword!1", id="empty-identity"),
    pytest.param("qa.invalid.user@example.com", "", id="empty-password"),
    pytest.param("' OR '1'='1", "' OR '1'='1", id="sql-injection-attempt"),
    pytest.param("   ", "   ", id="whitespace-only"),
]
