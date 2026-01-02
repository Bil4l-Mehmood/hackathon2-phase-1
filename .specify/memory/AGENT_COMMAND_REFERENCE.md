# Agent Command Reference: Constitution-Aligned Workflow

**Quick reference for agents implementing the Evolution of Todo project**

---

## Before Every Task

### Verification Checklist

```bash
# 1. Is this task in approved spec?
❓ Specification exists: specs/<feature-name>/spec.md
❓ Specification is approved: user sign-off documented
❓ Task is in approved tasks: specs/<feature-name>/tasks.md
❓ Task is in current phase: Phase I/II/III/IV/V

# 2. Is this constitutional?
❓ Technology stack matches Part IV: EVOLUTION_CONSTITUTION.md
❓ No phase boundary violations: Part III
❓ No forbidden actions: Part II.1
❓ Follows spec-first workflow: Part I

# 3. Is everything ready?
❓ Tests written (Red phase)
❓ Spec references documented
❓ Plan reviewed
❓ No surprises or scope creep detected
```

---

## Workflow Commands

### 1. Constitution Review
```
ACTION: Read constitution
WHEN: Starting new phase or new agent assignment
FILE: .specify/memory/EVOLUTION_CONSTITUTION.md
TIME: 10 minutes
VERIFY: [Constitution Usage Guide](./.specify/memory/CONSTITUTION_USAGE_GUIDE.md)
```

### 2. Specification Review
```
ACTION: Read specification
WHEN: Before implementation task
FILE: specs/<feature-name>/spec.md
VERIFY:
  - Acceptance criteria clear
  - Scope boundaries defined
  - User approval documented
```

### 3. Architecture Plan Review
```
ACTION: Read architecture plan
WHEN: Before implementation task
FILE: specs/<feature-name>/plan.md
VERIFY:
  - Design decisions documented
  - Rationale clear
  - User approval documented
```

### 4. Task Review
```
ACTION: Read task breakdown
WHEN: Before implementation task
FILE: specs/<feature-name>/tasks.md
VERIFY:
  - Task is testable
  - Success criteria defined
  - Phase assignment correct
  - No scope creep
```

### 5. Red Phase (Write Failing Tests)
```
WHEN: After all specs/plans/tasks approved

PROCESS:
1. Read the approved task
2. Write test to specification
3. Verify test fails (no implementation yet)
4. Document test in task
5. Get user approval on tests
```

### 6. Green Phase (Minimal Implementation)
```
WHEN: After Red phase approval

PROCESS:
1. Implement exactly to spec
2. No features beyond spec
3. No refactoring of unrelated code
4. Tests must pass
5. Code references spec/task
6. All tests green
```

### 7. Refactor Phase (Optimize with Tests Passing)
```
WHEN: All tests green

PROCESS:
1. Improve code within passing tests
2. No new features
3. No scope expansion
4. All tests remain green
5. Clean architecture maintained
6. Minimal, focused changes
```

### 8. PHR Creation (Post-Implementation)
```
WHEN: Implementation complete

CREATE: history/prompts/<category>/<ID>-<slug>.<stage>.prompt.md

FILL:
  id: <next ID>
  title: <3-7 words>
  stage: <red|green|refactor>
  date: <YYYY-MM-DD>
  files: <list created/modified>
  prompt_text: <user request verbatim>
  response_text: <key artifacts>
```

### 9. ADR Creation (If Significant Decision)
```
WHEN: Architectural decision with:
  - Long-term consequences, OR
  - Multiple alternatives considered, OR
  - Cross-cutting influence

CREATE: history/adr/<decision-title>.md

FILL:
  Title: [Decision]
  Status: Proposed/Accepted/Deprecated
  Context: Why this decision?
  Decision: What was decided?
  Rationale: Why this option?
  Alternatives: Other options considered
  Consequences: What changes?
  Phase Introduced: Phase N
```

---

## Agent Do's and Don'ts

### ✅ DO

- **Read the constitution first** — It's the source of truth
- **Verify spec/plan/tasks approved** — Never skip this step
- **Write tests first** — Red-Green-Refactor strictly
- **Reference spec in code** — Link implementation to requirements
- **Isolate database logic** — Keep clean architecture
- **Document decisions** — Create ADRs for significant choices
- **Create PHRs post-work** — Capture what was done
- **Ask for clarification** — If spec is unclear, ask user
- **Maintain test coverage** — Minimum 80% per spec
- **Respect phase boundaries** — No future features in past phases

### ❌ DON'T

- **Add features not in spec** — FORBIDDEN (Part II.1)
- **Refactor unrelated code** — Only what's specified
- **Skip specification phase** — Constitution enforces Spec-First
- **Hardcode configuration** — Use environment variables
- **Ignore test failures** — All tests must pass
- **Write comments on unchanged code** — Only modified code
- **Change spec to match code** — Spec wins always
- **Use unapproved technology** — Check Part IV of constitution
- **Implement future-phase features** — Respect phase boundaries
- **Make architectural decisions alone** — Suggest ADRs for approval

---

## Quick Decision Tree

```
Question: "Can I add [feature]?"

├─ Is it in the approved spec?
│  ├─ Yes → Can I implement it in current phase?
│  │       ├─ Yes → Proceed (Red-Green-Refactor)
│  │       └─ No → Wait for that phase
│  └─ No → Stop. Ask user to amend spec.
└─ No → Stop. Ask user to add to spec.
```

```
Question: "Can I refactor [code]?"

├─ Is there a failing test?
│  ├─ Yes → Refactor to fix it (Refactor phase)
│  └─ No → Don't touch it
└─ No → Don't touch it
```

```
Question: "Can I use [technology]?"

├─ Check Part IV of EVOLUTION_CONSTITUTION.md
│  ├─ Is it in approved phase?
│  │  ├─ Yes → You can use it
│  │  └─ No → You cannot use it yet
│  └─ Is it allowed?
│     ├─ Yes → Use it
│     └─ No → Propose amendment
└─ Not listed? Propose amendment.
```

---

## File Structure for New Work

When starting a new feature:

```
Create these files in order:

1. specs/<feature-name>/spec.md
   ✅ Get user approval

2. specs/<feature-name>/plan.md
   ✅ Get user approval

3. specs/<feature-name>/tasks.md
   ✅ Get user approval

4. Code implementation (backend or frontend)
   - Write failing tests (Red)
   - Implement code (Green)
   - Refactor code (Refactor)

5. history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md
   ✅ Document work after completion

6. (Optional) history/adr/<decision-title>.md
   ✅ If significant architectural decision
```

---

## Phase Specification Templates

### Phase I: Core API

```
Specification:
  - REST API endpoints (CRUD)
  - User authentication
  - Database schema
  - Error handling
  - Test coverage (80%+)

Technology:
  - Python, FastAPI, SQLModel, PostgreSQL

Tasks:
  1. Setup project structure
  2. Implement user model
  3. Implement todo model
  4. Implement CRUD endpoints
  5. Implement authentication
  6. Write integration tests
```

### Phase II: Web UI

```
Specification:
  - Next.js application
  - React components
  - Integration with Phase I API
  - User authentication UI
  - Todo management UI

Technology:
  - Next.js, TypeScript, Tailwind CSS

Tasks:
  1. Setup Next.js project
  2. Create layout components
  3. Implement authentication flow
  4. Implement todo listing
  5. Implement todo creation
  6. Write integration tests
```

### Phase III: Real-Time

```
Specification:
  - WebSocket integration
  - Kafka event streaming
  - Advanced queries
  - Full-text search

Technology:
  - Kafka, WebSockets, Advanced PostgreSQL

Tasks:
  1. Setup Kafka cluster
  2. Implement event producers
  3. Implement WebSocket handlers
  4. Implement search functionality
  5. Optimize queries
  6. Write integration tests
```

### Phase IV: AI Agents

```
Specification:
  - OpenAI integration
  - Agent-driven features
  - Natural language processing
  - MCP servers

Technology:
  - OpenAI SDK, MCP servers

Tasks:
  1. Setup OpenAI integration
  2. Implement agent framework
  3. Create MCP servers
  4. Implement NLP features
  5. Add safety guardrails
  6. Write agent tests
```

### Phase V: Cloud-Native

```
Specification:
  - Microservices architecture
  - Kubernetes deployment
  - Dapr service mesh
  - Observability stack

Technology:
  - Docker, Kubernetes, Dapr

Tasks:
  1. Containerize services
  2. Create Kubernetes manifests
  3. Setup Dapr
  4. Implement health checks
  5. Setup observability
  6. Test deployment
```

---

## Common Commands

### Read Constitution
```
File: .specify/memory/EVOLUTION_CONSTITUTION.md
Time: 10-15 minutes
Then: Review Part II (Agent Behavior) and Part IV (Tech Stack)
```

### Read Usage Guide
```
File: .specify/memory/CONSTITUTION_USAGE_GUIDE.md
Time: 5 minutes
When: Confused about a rule or unsure about allowed actions
```

### Create Specification
```
Template: .specify/templates/spec-template.md
Location: specs/<feature-name>/spec.md
Reference: EVOLUTION_CONSTITUTION.md Part I
```

### Create Plan
```
Template: .specify/templates/plan-template.md
Location: specs/<feature-name>/plan.md
Reference: EVOLUTION_CONSTITUTION.md Part VI
```

### Create Tasks
```
Template: .specify/templates/tasks-template.md
Location: specs/<feature-name>/tasks.md
Reference: EVOLUTION_CONSTITUTION.md Part VI
```

### Create PHR
```
Template: .specify/templates/phr-template.prompt.md
Location: history/prompts/<category>/<ID>-<slug>.<stage>.prompt.md
Reference: EVOLUTION_CONSTITUTION.md Part VII
```

### Create ADR
```
Template: .specify/templates/adr-template.md
Location: history/adr/<title>.md
Reference: EVOLUTION_CONSTITUTION.md Part VIII
```

---

## Compliance Checklist (Quick)

### Pre-Implementation
- [ ] Constitution reviewed
- [ ] Specification exists and approved
- [ ] Plan exists and approved
- [ ] Tasks exist and approved
- [ ] Technology stack constitutional
- [ ] Phase boundaries clear

### Implementation
- [ ] Tests written first (Red)
- [ ] Code matches spec (Green)
- [ ] All tests passing
- [ ] Refactoring focused (Refactor)
- [ ] Clean architecture maintained

### Post-Implementation
- [ ] All tests pass (80%+)
- [ ] PHR created
- [ ] ADRs created (if needed)
- [ ] Code reviews passed
- [ ] User approval obtained

---

## Getting Unstuck

**Problem**: "Specification is unclear"
**Solution**: Document the gap, ask user for clarification, update spec

**Problem**: "Spec doesn't match what I'm trying to build"
**Solution**: Don't change code. Change spec. Get approval. Resume.

**Problem**: "I found a bug in unrelated code"
**Solution**: Document it, create a new task, get approval, fix later

**Problem**: "I think we need [new feature]"
**Solution**: Document in spec, propose to user, update spec, get approval

**Problem**: "Phase boundaries aren't clear"
**Solution**: Check EVOLUTION_CONSTITUTION.md Part III, or ask user

**Problem**: "Can I use [technology]?"
**Solution**: Check Part IV of constitution. If not listed, propose amendment.

---

**Remember**: Constitutional compliance is not optional. The Constitution is the supreme law.

For questions, refer to:
1. EVOLUTION_CONSTITUTION.md
2. CONSTITUTION_USAGE_GUIDE.md
3. This file (AGENT_COMMAND_REFERENCE.md)
4. Ask the user

---

**Last Updated**: 2025-12-30
