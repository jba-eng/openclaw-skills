---
name: test-driven-development
description: Use when writing new code or adding functionality. Enforces strict RED → GREEN → REFACTOR cycle. Code written before a failing test gets deleted.
---

# Test-Driven Development

## The Rule

**RED → GREEN → REFACTOR. In that order. No exceptions.**

1. Write a failing test FIRST
2. Run it to see it fail
3. Write MINIMAL code to make it pass
4. Run to verify it passes
5. Refactor if needed
6. Commit

## Process

### Step 1: Write Failing Test

```python
def test_add_numbers():
    result = add(2, 3)
    assert result == 5
```

Run it. It MUST fail with "add not defined" or assertion error.

### Step 2: Write Minimal Implementation

```python
def add(a, b):
    return 5  # Hardcode first - don't solve the general case yet
```

Run test. It MUST pass.

### Step 3: Make It Real

```python
def add(a, b):
    return a + b
```

Run test. It MUST pass.

### Step 4: Refactor

- Clean up code
- Improve names
- Remove duplication
- Run tests after each change

## Anti-Patterns

**NEVER do these:**
- Write implementation code before test
- Write full implementation in one go
- Skip the "failing test" step
- Move on without tests passing
- Skip refactoring

## If You Write Code Before a Test

**Delete it.** Start over with the test.

## What To Test

- Happy path
- Edge cases
- Error conditions
- Boundary values