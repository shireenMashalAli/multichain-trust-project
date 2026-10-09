from trust_utils import update_trust_score

tests = [
    (98, True, 100),
    (5, False, 0),
    (50, True, 55),
    (50, False, 40),
    (0, False, 0),
    (100, True, 100),
]

passed = 0

for current, reliable, expected in tests:
    actual = update_trust_score(current, reliable)

    if actual == expected:
        print(
            f"PASS: score={current}, reliable={reliable}, "
            f"result={actual}"
        )
        passed += 1
    else:
        print(
            f"FAIL: score={current}, reliable={reliable}, "
            f"expected={expected}, got={actual}"
        )

print(f"\nResults: {passed}/{len(tests)} tests passed.")