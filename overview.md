# Advent of Code 2024 - as LLM benchmark

I want to test differnt LLM's coding capabilities using the Advent of Code.

## Methodology
To ensure comparability of the models, I use the same promt for all models. The initial prompt is:
```
Please solve the following problem using Python, assuming that the provided input is in a file named input.txt.
```
This prompt is followed by the copied problem description of this day's exercise.

The models are rated on 0-shot prompting. If this does not work, they are being prompted with the information that AoC provides, whether the result is too high or too low and have a chance of fixing their solution up to four times to a total of five tries. If they don't manage to provide a working solution within 5 tries, this day is marked as failed. Otherwise, the number of tries is noted.

## Overview
| Day | Claude 3.5 Sonnet 20241022 | GPT 4o | Qwen Coder 32B |
| --- | --- | --- | --- |
| 01 | x | | |
| 02 | x | | |
| 03 | x | | |
| 04 | 1/- | | |