from passguard.checker import analyze, entropy_bits


def test_common_password_is_flagged() -> None:
    result = analyze("password")

    assert any("common-password" in issue for issue in result["issues"])


def test_short_password_is_weak() -> None:
    assert analyze("Ab1!")["rating"] == "Weak"


def test_complex_example_is_strong() -> None:
    assert analyze("v9#Lq!2xTz@8mWp")["rating"] == "Strong"


def test_entropy_increases_with_length() -> None:
    assert entropy_bits("Aa1!") < entropy_bits("Aa1!Bb")


def test_empty_password_has_zero_entropy() -> None:
    assert entropy_bits("") == 0.0
