# Prompt templates used for explanation, refactor, and test generation.
EXPLAIN_PROMPT = """You are an expert senior software engineer. Given the following code, provide:
1) A concise explanation of what the code does (2-4 sentences).
2) Important implementation details or pitfalls to watch out for.
3) Time & space complexity analysis (if applicable).
4) A short list of refactoring suggestions (3 items max).

Return the result as a JSON object with keys: explanation, details, complexity, refactors.

Code:
```python
{code}
```"""

TEST_PROMPT = """You are an expert software developer and unit-test author. Given the following Python function(s)/module, generate a set of pytest unit test stubs that cover:
- Typical cases
- Edge cases
- Error/exception cases (where applicable)

Return only valid Python code suitable for a pytest file (do NOT include markdown or explanations). Use simple assert statements or pytest.raises where necessary.

Code:
```python
{code}
```"""
