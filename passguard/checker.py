import math
import re
import string

_COMMON_PASSWORDS = {
    "password",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
    "abc123",
    "password1",
}
_YEAR_PATTERN = re.compile(r"(?:19|20)\d{2}")
_REPEATED_PATTERN = re.compile(r"(.)\1{2,}", re.DOTALL)
_GUESSES_PER_SECOND = 1e10
_SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60


def entropy_bits(pw: str) -> float:
    if not pw:
        return 0.0

    pool_size = 0
    if any(char in string.ascii_lowercase for char in pw):
        pool_size += 26
    if any(char in string.ascii_uppercase for char in pw):
        pool_size += 26
    if any(char in string.digits for char in pw):
        pool_size += 10
    if any(char not in string.ascii_letters + string.digits for char in pw):
        pool_size += 32

    return round(len(pw) * math.log2(pool_size), 1)


def crack_time(bits: float) -> str:
    log2_seconds = bits - 1 - math.log2(_GUESSES_PER_SECOND)
    if log2_seconds < 0:
        return "<1 second"

    if log2_seconds < math.log2(60):
        return f"{math.exp2(log2_seconds):.1f} seconds"
    if log2_seconds < math.log2(60 * 60):
        return f"{math.exp2(log2_seconds - math.log2(60)):.1f} minutes"
    if log2_seconds < math.log2(24 * 60 * 60):
        return f"{math.exp2(log2_seconds - math.log2(60 * 60)):.1f} hours"
    if log2_seconds < math.log2(_SECONDS_PER_YEAR):
        return f"{math.exp2(log2_seconds - math.log2(24 * 60 * 60)):.1f} days"
        log2_seconds -= math.log2(boundary)
    # Keep very large estimates readable without overflowing a float.
    log10_years = (
        bits - 1 - math.log2(_GUESSES_PER_SECOND) - math.log2(_SECONDS_PER_YEAR)
    ) * math.log10(2)
    exponent = math.floor(log10_years)
    if exponent < 3:
        return f"{10**log10_years:.1f} years"
    mantissa = 10 ** (log10_years - exponent)
    return f"{mantissa:.2f}e{exponent} years"


def analyze(pw: str) -> dict[str, float | str | list[str]]:
    bits = entropy_bits(pw)
    lowered = pw.lower()
    issues: list[str] = []

    if len(pw) < 12:
        issues.append("Use at least 12 characters.")
    if lowered in _COMMON_PASSWORDS:
        issues.append("This password is in the common-password blocklist.")
    if _REPEATED_PATTERN.search(pw):
        issues.append("Contains a character repeated three or more times.")
    if any(sequence in lowered for sequence in ("abc", "123", "qwe", "pass")):
        issues.append("Contains a predictable sequence.")
    if _YEAR_PATTERN.search(pw):
        issues.append("Contains a year-like pattern.")

    if issues and bits >= 60:
        bits -= 20

    rating = "Weak" if bits < 40 else "Moderate" if bits < 60 else "Strong"
    return {
        "entropy_bits": bits,
        "rating": rating,
        "crack_time": crack_time(bits),
        "issues": issues,
    }
