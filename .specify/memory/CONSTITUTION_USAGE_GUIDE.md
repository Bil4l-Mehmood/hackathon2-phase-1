# Evolution of Todo: Constitution Usage Guide

**How to use and enforce the Global Constitution in daily development**

---

## Quick Start: The Five-Step Workflow

Every task must follow this workflow:

### Step 1: Constitution Alignment ✅
- Verify the change aligns with `EVOLUTION_CONSTITUTION.md`
- Check technology stack constraints (Part IV)
- Verify phase boundaries (Part III)
- Confirm no forbidden actions (Part II.1)

### Step 2: Specification ✅
- Create or update specification in `specs/<feature>/spec.md`
- Include acceptance criteria
- Include scope boundaries
- **Get user approval**

### Step 3: Plan ✅
- Create or update plan in `specs/<feature>/plan.md`
- Include architectural decisions
- Suggest relevant ADRs
- **Get user approval**

### Step 4: Tasks ✅
- Create or update tasks in `specs/<feature>/tasks.md`
- Break into testable units
- Assign to correct phase
- **Get user approval**

### Step 5: Implement ✅
- Write failing tests (Red)
- Implement to pass tests (Green)
- Refactor with tests passing (Refactor)
- Create PHR documenting work
- Suggest ADRs if significant decisions made

---

## Key Rules to Enforce

### Rule 1: No Code Without Spec ⛔
```
If asked: "Can you add [feature]?"
Response: "Show me the approved specification first."
```

### Rule 2: Spec Drives Code, Not Vice Versa ⛔
```
If code doesn't match spec: Change code
If code reveals spec gap: Change spec (code waits)
Never: Change spec to match code
```

### Rule 3: No Feature Invention ⛔
```
Forbidden: "Let me also optimize the database"
Forbidden: "Let me add error handling for this edge case"
Forbidden: "Let me improve the architecture"
Required: All changes must be in approved spec/tasks
```

### Rule 4: No Code-Level Refinement ⛔
```
Forbidden: Refactor unrelated code
Forbidden: Add comments to unchanged code
Forbidden: Clean up error handling beyond spec
Allowed: Only changes specified in tasks
```

### Rule 5: Respect Phase Boundaries ⛔
```
Phase II feature cannot appear in Phase I code
Phase III Real-time cannot appear in Phase II
All architecture evolution must go through spec amendment
```

### Rule 6: Technology Stack Is Fixed ⛔
```
Cannot substitute: Python → Node.js (without amendment)
Cannot add: Redis (without spec approval)
Cannot remove: PostgreSQL (without amendment)
See Part IV of constitution for full tech matrix
```

---

## Constitutional Compliance Checklist

Use this **before every implementation task**:

### Pre-Implementation
- [ ] Constitution reviewed (Part I-II)
- [ ] Specification exists and is approved
- [ ] Specification includes acceptance criteria
- [ ] Plan exists and is approved
- [ ] Tasks exist and are approved
- [ ] Phase assignment is correct
- [ ] Technology stack is constitutional
- [ ] No phase boundary violations

### During Implementation
- [ ] Tests written first (Red phase)
- [ ] Code implements spec exactly
- [ ] No features added beyond spec
- [ ] All tests passing (Green phase)
- [ ] Code references spec/tasks
- [ ] Database layer isolated (clean architecture)
- [ ] Refactoring within passing tests only

### Post-Implementation
- [ ] All tests pass (80%+ coverage)
- [ ] Code matches spec exactly
- [ ] PHR created and complete
- [ ] ADRs documented if needed
- [ ] Phase boundaries maintained
- [ ] Technology stack compliant
- [ ] Ready for user review

---

## Common Violations & How to Fix Them

### Violation 1: Adding Features Not in Spec
```
❌ Agent: "I'll add caching to improve performance"
✅ Correct: "This isn't in the spec. Should we amend the spec?"
```

**Fix**:
1. Stop implementation
2. Document feature in specification
3. Get user approval
4. Resume implementation

### Violation 2: Code-Level Refinement
```
❌ Agent: "While implementing, let me clean up this related function"
✅ Correct: "That's outside the spec. Capture it in a new task."
```

**Fix**:
1. Don't touch unrelated code
2. If improvement is needed, add to tasks
3. Get user approval for new task
4. Resume after spec amendment

### Violation 3: Phase Leakage
```
❌ Agent: "I'll add WebSockets now (Phase III) while in Phase I"
✅ Correct: "WebSockets are Phase III only. Phase I is REST only."
```

**Fix**:
1. Remove Phase III code from Phase I
2. Ensure Phase I implements only Phase I spec
3. Wait for Phase III specification
4. Resume Phase III work when time comes

### Violation 4: Technology Substitution
```
❌ Agent: "Let's use MongoDB instead of PostgreSQL"
✅ Correct: "PostgreSQL is constitutional. MongoDB requires amendment."
```

**Fix**:
1. Stick with PostgreSQL
2. If change is needed, start amendment process
3. Document rationale in proposed amendment
4. Get user approval
5. Update constitution
6. Resume with approved technology

### Violation 5: No Spec Approval
```
❌ Agent: "I'm starting implementation now"
✅ Correct: "Specification approved? Plan approved? Tasks approved?"
```

**Fix**:
1. Stop implementation
2. Create specification document
3. Get user approval
4. Create plan document
5. Get user approval
6. Create tasks document
7. Get user approval
8. Then resume implementation

---

## Documenting Work

### Prompt History Records (PHRs)

Create after every significant work session:

**Location**: `history/prompts/<category>/<ID>-<slug>.<stage>.prompt.md`

**Categories**:
- `constitution/` — Constitutional changes
- `<feature-name>/` — Feature work (spec, plan, tasks, red, green, refactor)
- `general/` — General inquiries

**Stages**:
- `spec` — Specification work
- `plan` — Architecture planning
- `tasks` — Task breakdown
- `red` — Writing failing tests
- `green` — Implementing code
- `refactor` — Code optimization
- `general` — Other work

### Architectural Decision Records (ADRs)

Create when significant architectural decisions are made:

**Location**: `history/adr/<title>.md`

**When to create**:
- ✅ Decision has long-term consequences
- ✅ Multiple options were considered
- ✅ Decision influences multiple components

**What to document**:
- Context: Why this decision was needed
- Decision: What was decided and why
- Rationale: Why this option over others
- Alternatives: Other options considered
- Consequences: What changes as a result

---

## Phase Reference

Quick reminder of phase scope:

| Phase | Scope | NOT in Scope | Key Tech |
|-------|-------|-------------|----------|
| I | Core API, CRUD, Auth | UI, Real-time | Python, FastAPI, PostgreSQL |
| II | Web UI, Integration | Real-time, Advanced features | Next.js, TypeScript |
| III | Real-time, Search, Advanced queries | Microservices, Dapr | Kafka, WebSockets |
| IV | AI Agents, OpenAI integration | Full cloud-native | OpenAI SDK, MCP |
| V | Microservices, Kubernetes, Dapr | Multi-region | Docker, K8s, Dapr |

---

## When to Amend the Constitution

Amendments are needed when:

1. **Gap Exists**: Constitution has no guidance on required topic
2. **Ambiguity**: Current guidance is unclear or conflicting
3. **Evolution**: Project needs significant architectural shift
4. **Technology Change**: Stack substitution required

Amendment process:
1. Propose change to constitution
2. Document rationale
3. Get user approval
4. Update `EVOLUTION_CONSTITUTION.md`
5. Create PHR documenting amendment
6. Resume work with updated constitution

---

## Enforcement Strategy

### For Agents
- Every task starts with constitution review
- Every implementation verifies spec alignment
- Every PR references spec/tasks
- Every ADR documents significant decisions

### For Users
- Review specifications for completeness
- Review plans for architectural soundness
- Review tasks for testability
- Review code for spec compliance

### For the Project
- PHRs create audit trail of decisions
- ADRs explain architectural choices
- Constitution is source of truth
- All changes are traceable to spec

---

## Success Indicators

You're following the constitution when:

✅ All code references specifications
✅ No features appear that aren't in spec
✅ Phase boundaries are maintained
✅ Technology stack is consistent
✅ All major decisions are documented in ADRs
✅ PHRs form complete history of work
✅ Tests verify spec compliance
✅ Code changes are minimal and focused
✅ Refactoring is systematic
✅ Clean architecture is maintained

---

## Getting Help

**Question**: "Can I add this feature?"
**Answer**: Check the approved specification. If it's there, proceed. If not, amend the spec first.

**Question**: "Should I refactor this code?"
**Answer**: Is there a test failure? Yes → refactor. No → leave it alone.

**Question**: "Can I use technology X?"
**Answer**: Check Part IV of the constitution. If it's allowed for your phase, yes. Otherwise, propose an amendment.

**Question**: "What if the spec is unclear?"
**Answer**: Document the gap, propose clarification, get user approval, update the spec.

**Question**: "Do I need an ADR?"
**Answer**: Will this decision affect the system long-term? Did I consider alternatives? Does it cross multiple components? If yes to all, create an ADR.

---

**Remember**: The Constitution is the supreme law. When in doubt, defer to the Constitution.
