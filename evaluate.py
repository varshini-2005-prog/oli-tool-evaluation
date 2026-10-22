
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
    test_file = Path("test_cases.json")

    if not test_file.exists():
        print("Error: test_cases.json was not found.")
        sys.exit(1)

    with test_file.open(encoding="utf-8") as file:
        test_cases = json.load(file)

    if len(sys.argv) < 2:
        print("Usage: python evaluate.py task1_transcript.json")
        sys.exit(0)

    transcript_path = Path(sys.argv[1])

    if not transcript_path.exists():
        print(f"Error: transcript file not found: {transcript_path}")
        sys.exit(1)

    with transcript_path.open(encoding="utf-8") as file:
        transcript = json.load(file)

    actual_by_id = {
        str(item["id"]): item.get("actual_tool_calls", [])
        for item in transcript
    }

    passed_count = 0
    evaluated_count = 0
    total_correct = 0
    total_missing = 0
    total_unexpected = 0

    for case in test_cases:
        case_id = str(case["id"])

        # No real transcript for this request: do not score it.
        if case_id not in actual_by_id:
            print(f"\nCase {case_id}: NOT EVALUATED")
            print("  Reason: No matching transcript entry.")
            continue

        result = score_case(
            case["expected_tool_calls"],
            actual_by_id[case_id]
        )

        evaluated_count += 1
        passed_count += int(result["passed"])
        total_correct += len(result["correct"])
        total_missing += len(result["missing"])
        total_unexpected += len(result["unexpected"])

        status = "PASS" if result["passed"] else "FAIL"
        print(f"\nCase {case_id}: {status}")
        print("  Correct:", result["correct"])
        print("  Missing:", result["missing"])
        print("  Unexpected:", result["unexpected"])
        print(f"  Precision: {result['precision']:.2f}")
        print(f"  Recall: {result['recall']:.2f}")

    print("\n=== SUMMARY ===")
    print(f"Cases in test set: {len(test_cases)}")
    print(f"Cases evaluated: {evaluated_count}")
    print(f"Cases not evaluated: {len(test_cases) - evaluated_count}")
    print(f"Cases passed: {passed_count}/{evaluated_count}")
    print(f"Correct calls: {total_correct}")
    print(f"Missing calls: {total_missing}")
    print(f"Unexpected calls: {total_unexpected}")


if __name__ == "__main__":
    main()
