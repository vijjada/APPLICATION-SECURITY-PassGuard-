import getpass

from passguard.checker import analyze


def main() -> None:
    password = getpass.getpass("Password to assess (input hidden): ")
    result = analyze(password)

    print(f"Rating: {result['rating']}")
    print(f"Estimated entropy: {result['entropy_bits']} bits")
    print(f"Estimated average crack time: {result['crack_time']}")
    issues = result["issues"]
    if issues:
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Issues: none detected")


if __name__ == "__main__":
    main()
