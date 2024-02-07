# Instruction Chain Programming Contest

> KoH

http://10.102.100.20/

# Instruction Chain Programming Contest (ICPC)

## Links

- [A + B Problem](./src/A%20+%20B%20Problem.md)
- [Find Range](./src/Find%20Range.md)
- [A + B Revenge](./src/A%20+%20B%20Revenge.md)
- Sort

## Rules

- Your goal is to write x86_64 shellcode to solve problems.
- At the end of every round, your latest submission is judged on multiple test cases and your score is calculated.
- You can choose a byte to ban. All other teams cannot use the byte you banned in their shellcode in the next round. You can still use the byte unless another team also bans it.
- You can view other teams' submissions from at least 1 round ago. However, the order of bytes in their shellcode are randomly shuffled.

## Scoring

- If you use a banned byte in a round, your submission is automatically incorrect.
- If your submission uses too much time or memory, or doesn't exit correctly (for example, a segmentation fault), it is considered incorrect.
Your submission needs to return the correct answer for every test case to be considered correct.
- For each problem:
    - If your shellcode is incorrect for any test case, you get 0 score.
    - Otherwise, let L1 be the length of the length of the shortest correct shellcode out of all teams, and L2 be the length of your correct shellcode. You get L1/L2 score for the problem, rounded to 3 decimal places.
    - If every team is incorrect, every team gets 0 score.
    The KoH ranking is given according to the sum of scores of all problems.

## Technical

- Your shellcode is called as a function using the standard System V ABI. Remember to return from the function.
- The running environment is an Ubuntu 22.04 Docker image without additional packages.
- In each problem, a "grader" program is responsible for loading and executing your shellcode. You can download graders from problem statements.
- We use [isolate](https://github.com/ioi/isolate) to restrict the grader and measure time and memory. If your submission does weird actions, please test if they are blocked by isolate before submitting.
