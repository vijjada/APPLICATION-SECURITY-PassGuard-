import hashlib
import time

import bcrypt

_DEMO_PASSWORD = "Example#Pass2024"


def main() -> None:
    # This intentionally demonstrates an insecure digest (OWASP A02).
    for _ in range(2):
        digest = hashlib.md5(
            _DEMO_PASSWORD.encode(), usedforsecurity=False
        ).hexdigest()  # nosec B324
        print(f"MD5 (unsalted): {digest}")

    bcrypt_hashes = []
    for number in (1, 2):
        started = time.perf_counter()
        hashed = bcrypt.hashpw(
            _DEMO_PASSWORD.encode(), bcrypt.gensalt(rounds=12)
        )
        elapsed = time.perf_counter() - started
        bcrypt_hashes.append(hashed)
        print(f"bcrypt hash {number}: {hashed.decode()}")
        print(f"bcrypt hashing time {number}: {elapsed:.3f} seconds")

    verified = bcrypt.checkpw(_DEMO_PASSWORD.encode(), bcrypt_hashes[0])
    print(f"bcrypt verification: {verified}")


if __name__ == "__main__":
    main()
