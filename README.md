# Oli Tool Evaluation

This project evaluates whether an AI assistant selects appropriate tools for realistic creator requests.

## Project goals
- Create 20 realistic creator requests.
- Define expected tool calls for each request.
- Score assistant tool-call transcripts using Python.
- Report correct, missing, and unexpected tool calls.

## Evaluation method
The scoring script compares expected tool calls with actual tool calls in a transcript.

## Limitations
Results depend on the accuracy of the expected tool calls and the availability of a genuine transcript. Sample data will be labelled clearly and will not be presented as a real Oli transcript.

## What it found

### Initial sample run

The evaluator ran successfully against a sample transcript.

- Test cases defined: 20
- Sample cases with recorded tool calls: 3
- Cases passed: 2/20
- Correct tool calls: 3
- Missing expected tool calls: 25
- Unexpected tool calls: 0

The first two cases passed. The third case failed because the sample transcript did not contain the expected `list_my_deals` call. The remaining cases also lacked recorded calls.

**Limitation:** This is a plumbing test using sample data, not a measurement of Oli's real performance. A genuine Task 1 transcript must be evaluated before drawing conclusions about the assistant.
