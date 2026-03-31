# {FEATURE_NAME} Tasks

## T1: {TASK_DESCRIPTION}

**Status**: planned

**Dependencies**: None

**Done When**: 
- {CONDITION_1}
- {CONDITION_2}
- {CONDITION_3}

**Estimated Effort**: {TIME_ESTIMATE}

---

## T2: {TASK_DESCRIPTION}

**Status**: planned

**Dependencies**: T1

**Done When**: 
- {CONDITION_1}
- {CONDITION_2}

**Estimated Effort**: {TIME_ESTIMATE}

---

## T3: {TASK_DESCRIPTION}

**Status**: planned

**Dependencies**: T1, T2

**Done When**: 
- {CONDITION_1}
- {CONDITION_2}
- {CONDITION_3}

**Estimated Effort**: {TIME_ESTIMATE}

---

## Task Status Legend

- **planned**: Not started yet
- **in_progress**: Currently being worked on
- **blocked**: Waiting on dependencies or external factors
- **done**: Completed and verified
- **deferred**: Postponed to later phase

---

## done_when Best Practices

Good conditions are:
- **Testable**: Can be verified objectively
- **Specific**: Clear what needs to happen
- **Measurable**: Has clear success criteria

Examples:
- ✅ "API endpoint /api/users returns 200 status"
- ✅ "Unit tests pass with 80% coverage"
- ✅ "File src/auth.ts exists and exports login function"
- ✅ "Error message displays when email is invalid"

Avoid:
- ❌ "Code is good"
- ❌ "Feature works"
- ❌ "Implement properly"

---
*Created: {DATE}*
