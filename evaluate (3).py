import json
import sys
from pathlib import Path


def score_case(expected, actual):
    expected = set(expected)
    actual = set(actual)

    correct = expected & actual
    missing = expected - actual
    unexpected = actual - expected

    precision = len(correct) / len(actual) if actual else (
        1.0 if not expected else 0.0
    )
    recall = len(correct) / len(expected) if expected else (
        1.0 if not actual else 0.0
    )

    return {
        "correct": sorted(correct),
        "missing": sorted(missing),
        "unexpected": sorted(unexpected),
        "precision": precision,
        "recall": recall,
        "passed": not missing and not unexpected,
    }


def main():
    with open("test_cases.json", encoding="utf-8") as f:
        test_cases = json.load(f)

    if len(sys.argv) < 2:
        print("Usage: python evaluate.py task1_transcript.json")
        return

    with open(sys.argv[1], encoding="utf-8") as f:
        transcript = json.load(f)

    actual_by_id = {
        str(item["id"]): item.get("actual_tool_calls", [])
        for item in transcript
    }

    passed = 0
    evaluated = 0
    correct_total = 0
    missing_total = 0
    unexpected_total = 0

    for case in test_cases:
        case_id = str(case["id"])

        if case_id not in actual_by_id:
            print(f"\nCase {case_id}: NOT EVALUATED")
            print("  Reason: No matching transcript entry.")
            continue

        result = score_case(
            case["expected_tool_calls"],
            actual_by_id[case_id],
        )

        evaluated += 1
        passed += int(result["passed"])
        correct_total += len(result["correct"])
        missing_total += len(result["missing"])
        unexpected_total += len(result["unexpected"])

        status = "PASS" if result["passed"] else "FAIL"
        print(f"\nCase {case_id}: {status}")
        print("  Correct:", result["correct"])
        print("  Missing:", result["missing"])
        print("  Unexpected:", result["unexpected"])
        print(f"  Precision: {result['precision']:.2f}")
        print(f"  Recall: {result['recall']:.2f}")

    print("\n=== SUMMARY ===")
    print("Cases in test set:", len(test_cases))
    print("Cases evaluated:", evaluated)
    print("Cases not evaluated:", len(test_cases) - evaluated)
    print(f"Cases passed: {passed}/{evaluated}")
    print("Correct calls:", correct_total)
    print("Missing calls:", missing_total)
    print("Unexpected calls:", unexpected_total)


if __name__ == "__main__":
    main()
