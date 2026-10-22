# Creator Tool-Call Evaluation

## Overview
This project evaluates whether an AI assistant calls the expected tools when handling creator-related requests.

It contains 20 realistic creator requests, a Python evaluation script, and a real Task 1 transcript.

## Project Files
- `evaluate.py` — Evaluates expected and actual tool calls.
- `test_cases.json` — Contains the test cases and expected tool calls.
- `task1_transcript.json` — Contains the real transcript used for evaluation.
- `sample_transcript.json` — Provides a sample transcript for testing.

## Evaluation Metrics
- **Precision:** Proportion of actual tool calls that were expected.
- **Recall:** Proportion of expected tool calls that were made.
- **Missing calls:** Expected calls that were not made.
- **Unexpected calls:** Calls that were not expected.

Cases without a matching transcript are marked `NOT EVALUATED`.

## How to Run

Make sure Python is installed and all required JSON files are in the same directory.

```bash
python evaluate.py
```

## Results

The latest local evaluation reported:

- Total test cases: 20
- Cases evaluated: 1
- Cases not evaluated: 19
- Cases passed: 1/1
- Correct calls: 6
- Missing calls: 0
- Unexpected calls: 0
- Precision: 1.00
- Recall: 1.00

## Findings
The available real transcript matched all six expected tool calls. The evaluated case passed with no missing or unexpected calls.

The other 19 cases were marked `NOT EVALUATED` because matching transcripts were unavailable.

## Limitations
Only one of the 20 test cases was evaluated against a matching real transcript. Additional transcripts are required to assess the assistant's tool-selection performance across the full test set.
