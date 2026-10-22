
import json
import sys
from pathlib import Path


def score_case(expected, actual):
    """Compare expected and actual tool calls for one request."""
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

    # Supply actual tool calls as a JSON file path:
    # python evaluate.py actual_transcript.json
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py actual_transcript.json")
        print("Each transcript entry needs an id and actual_tool_calls.")
        print("Example: {\"id\": 1, \"actual_tool_calls\": [\"check_offer\"]}")
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
    total_correct = 0
    total_missing = 0
    total_unexpected = 0

    for case in test_cases:
        case_id = str(case["id"])
        actual = actual_by_id.get(case_id, [])
        result = score_case(case["expected_tool_calls"], actual)

        passed_count += int(result["passed"])
        total_correct += len(result["correct"])
        total_missing += len(result["missing"])
        total_unexpected += len(result["unexpected"])

        print(f"\nCase {case_id}: {'PASS' if result['passed'] else 'FAIL'}")
        print(f"  Correct: {result['correct']}")
        print(f"  Missing: {result['missing']}")
        print(f"  Unexpected: {result['unexpected']}")
        print(f"  Precision: {result['precision']:.2f}")
        print(f"  Recall: {result['recall']:.2f}")

    print("\n=== SUMMARY ===")
    print(f"Cases passed: {passed_count}/{len(test_cases)}")
    print(f"Correct calls: {total_correct}")
    print(f"Missing calls: {total_missing}")
    print(f"Unexpected calls: {total_unexpected}")


if __name__ == "__main__":
    main()
