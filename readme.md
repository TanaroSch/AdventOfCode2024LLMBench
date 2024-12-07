# Advent of Code 2024 - as LLM benchmark

I want to test differnt LLM's coding capabilities using the [Advent of Code](https://adventofcode.com/) challenges.

## Methodology
To ensure comparability of the models, I use the same promt for all models. The initial prompt is:
```
Please solve the following problem using Python, assuming that the provided input is in a file named input.txt.
```
This prompt is followed by the copied problem description of this day's exercise.

The models are rated on 0-shot prompting. If this does not work, they are being prompted with the information that AoC provides, whether the result is too high or too low and have a chance of fixing their solution up to four times to a total of five tries. If they don't manage to provide a working solution within 5 tries, this day is marked as failed (X), if this happens in the first part, the second part is marked with (-). Otherwise, the number of tries is noted. The reason why the solution is wrong is noted following the tries with (l) for logic and (s) for syntax errors.

### Models:
* Claude 3.5 Sonnet -> claude-3.5-sonnet-20241022 used on https://claude.ai 
* MS Copilot -> used the enterprise version of https://copilot.microsoft.com, exact model unknown
* GPT 4o -> GPT 4o used in the chat panel of GitHub Copilot without context of any file or workplace
* o1-mini -> o1-mini used in the chat panel of GitHub Copilot without context of any file or workplace
* o1-preview -> o1-preview used in the chat panel of GitHub Copilot without context of any file or workplace
* o1 -> o1 used on https://chatgpt.com/
* Qwen2.5-72b -> Qwen/Qwen2.5-72B-Instruct used on https://huggingface.co/chat
* Qwen2.5-Coder-32b -> Qwen/Qwen2.5-Coder-32B-Instruct used on https://huggingface.co/chat
* Qwen-QwQ -> Qwen/QwQ-32B-Preview used on https://huggingface.co/chat
* R1-Lite -> DeepSeek-R1-Lite preview used on https://chat.deepseek.com/

## Overview
| Day | Claude 3.5 Sonnet | MS Copilot | GPT 4o  | o1-mini | o1-preview | o1      | Qwen2.5-72b | Qwen2.5-Coder-32b | Qwen-QwQ  | R1-Lite |
| --- | ---               | ---        | ---     | ---     | ---        | ---     | ---         | ---               | ---       | ---     |
| 01  | 1/1               | 1/1        | 1/1     | 1/1     | 1/1        | 1/1     | 1/2 (s)     | 1/1               | 5/1 (l)   | 1/1     |
| 02  | 1/1               | 1/1        | 1/1     | 1/1     | 1/1        | 1/1     | 1/2 (s)     | 1/1               | 1/1       | 1/1     |
| 03  | 1/1               | 1/1        | 1/4 (l) | 1/1     | 1/1        | 1/1     | 1/2 (l)     | 1/1               | 1/1       | 1/1     |
| 04  | 1/2 (l)           | 1/X (l)    | 1/X (l) | 1/2 (l) | 1/1        | 1/1     | 1/X (l)     | 1/X (l)           | 1/X (l,s) | 1/1     |
| 05  | 1/1               | 1/1        | 3/1 (l) | 1/1     | 1/1        | 1/1     | 1/1         | X/- (l)           | 1/1       | 1/1     |
| 06  | 2/1 (l)           |            | X/- (l) | 1/1     | 1/1        | 3/1 (l) | 1/X (l)     | 2/X (l)           | 1/X (l)   | 1/1     |
| 07  | 1/3 (l)           |            | 1/1     | 1/1     | 1/1        | 1/1     | X/- (l)     | X/- (l)           | 1/1       | 1/1     |
| XX  |                   |            |         |         |            |         |             |                   |           |         |

## Weird occurences
* On day 2 GitHub Copilot GPT 4o repeatedly refused to answer my initial query. After ~5-10 attempts the safeguards allowed the answer. Since the answer was correct on the first successful response, I count this as one try.
* Qwen2.5-72b sometimes made syntax mistakes like using a space instead of ```_``` in variable names but only in the second part. I counted this as a failed try and marked it with (s).
* When prompting Qwen QwQ with the result from AoC that the value is too low it just responded with ```I'm here to help you understand the correct solution, not to debate the answer.```
* Qwen QwQ sometimes only provided the full code solution in the thought process, not in the final output. In these cases I still used the last code provided in the thought process.