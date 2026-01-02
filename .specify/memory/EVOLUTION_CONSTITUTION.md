# Evolution of Todo: Global Constitution

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Scope**: Phase I through Phase V

---

## Overview

This Constitution is the supreme governing document for the "Evolution of Todo" project across all five phases. It establishes mandatory principles, agent behavior rules, technology constraints, and quality standards that supersede all other documentation and requirements.

**Non-negotiable mandate**: All agents MUST operate within these constitutional boundaries. Deviations require explicit constitutional amendment.

---

## PART I: SPEC-DRIVEN DEVELOPMENT (MANDATORY)

### Principle: Specification-First Architecture

All development must strictly follow the immutable workflow:

```
Constitution → Specification → Tasks → Implementation
```

### 1.1 Pre-Implementation Requirements

Before ANY code is written, the following must exist and be APPROVED:

1. **Constitution Compliance Verification**
   - The change conforms to this Constitution
   - Technology stack is approved
   - Phase boundaries are respected

2. **Specification Document**
   - Location: `.specify/specs/<feature-name>/spec.md`
   - Must define WHAT is being built (not HOW)
   - Includes acceptance criteria and scope boundaries
   - User approval required before proceeding

3. **Architecture Plan**
   - Location: `.specify/specs/<feature-name>/plan.md`
   - Addresses HOW the feature will be implemented
   - Identifies architectural decisions
   - References relevant ADRs

4. **Task Breakdown**
   - Location: `.specify/specs/<feature-name>/tasks.md`
   - Each task is testable and independently verifiable
   - Clear success criteria for each task
   - Task assignment to specific phase

### 1.2 Spec-First Rules (Non-Negotiable)

- **No agent may write code without approved specifications**
  - Code written without spec is unconstitutional
  - Any unauthorized code must be removed immediately

- **No implementation begins before user sign-off**
  - Spec must be explicitly approved
  - Plan must be explicitly approved
  - Tasks must be explicitly approved

- **Specifications drive code, not vice versa**
  - If code doesn't match spec, spec wins (code changes)
  - If code reveals spec gaps, spec is amended (code waits)
  - No "quick fixes" without spec amendment

### 1.3 Spec Refinement Process

Refinements to requirements occur at the SPECIFICATION level, never in code:

1. Identify gap or change requirement in code review
2. Amend the specification document
3. Update the plan if architectural implications exist
4. Update task breakdown
5. Re-approve with user
6. Resume or restart implementation

---

## PART II: AGENT BEHAVIOR RULES

### 2.1 Forbidden Actions

The following are EXPLICITLY FORBIDDEN for all agents:

1. **Manual Coding by Humans**
   - Humans do not write production code
   - Humans define specifications only
   - Humans make architectural decisions
   - Agents implement from approved specifications

2. **Feature Invention**
   - Agents CANNOT add features not in approved spec
   - Agents CANNOT extend scope beyond specification
   - Agents CANNOT optimize "while they're at it"
   - Agents CANNOT add "future-proofing" features

3. **Specification Deviation**
   - Agents MUST implement exactly as specified
   - No "reasonable improvements" without spec amendment
   - No architectural decisions outside the plan
   - No technology substitutions without constitutional amendment

4. **Code-Level Refinement**
   - Agents CANNOT refactor specification-defined code
   - Agents CANNOT "clean up" unrelated code
   - Agents CANNOT add comments/docstrings to unmodified code
   - Agents CANNOT add error handling beyond specification

### 2.2 Required Agent Behaviors

1. **Specification Compliance Verification**
   - Every implementation task begins with spec validation
   - Agent must confirm spec exists and is approved
   - Agent must verify task is phase-appropriate

2. **Code Precision**
   - Code changes are minimal and focused
   - Each change references specific spec requirement
   - Changes are traceable to approved task

3. **Quality Assurance**
   - Agent must verify implementation matches spec
   - Agent must run tests before completion
   - Agent must document any spec-code mismatches

4. **Documentation Accuracy**
   - All PHRs (Prompt History Records) are created post-implementation
   - All architectural decisions are captured
   - All deviations from spec are flagged for amendment

---

## PART III: PHASE GOVERNANCE

### 3.1 Phase Definitions and Scope

The "Evolution of Todo" project is organized into five strictly-bounded phases:

#### Phase I: Core Todo API (Backend Foundation)
- **Scope**: Basic CRUD operations for todos, data persistence, user authentication
- **Not In Scope**: Frontend, real-time features, advanced querying, search
- **Technology**: Python, FastAPI, Neon PostgreSQL
- **Deliverable**: REST API with full test coverage

#### Phase II: Frontend Integration (UI Foundation)
- **Scope**: Next.js web UI, basic todo management, authentication integration
- **Not In Scope**: Real-time updates, offline mode, advanced filtering, collaboration
- **Technology**: Next.js, TypeScript, standard HTTP client
- **Deliverable**: Web application with basic functionality

#### Phase III: Advanced Features & Real-Time
- **Scope**: Real-time updates via Kafka/WebSockets, advanced querying, search, filtering
- **Not In Scope**: Microservices architecture, distributed tracing, AI features
- **Technology**: Kafka, WebSockets, improved API contracts
- **Deliverable**: Real-time capable application

#### Phase IV: AI-Powered Agents & OpenAI Integration
- **Scope**: OpenAI Agent SDK integration, intelligent task suggestions, natural language processing
- **Not In Scope**: Full microservices, Dapr, Kubernetes orchestration
- **Technology**: OpenAI Agents SDK, MCP servers
- **Deliverable**: AI-enhanced todo system

#### Phase V: Cloud-Native Microservices (Enterprise Scale)
- **Scope**: Microservices architecture, Kubernetes deployment, Dapr service mesh, full observability
- **Not In Scope**: Multi-region deployment, federated architecture, blockchain features
- **Technology**: Docker, Kubernetes, Dapr, comprehensive observability stack
- **Deliverable**: Enterprise-ready cloud-native platform

### 3.2 Phase Boundary Enforcement

- **No Feature Leakage**: Features defined for Phase N may NEVER be implemented in Phase N-1
  - Feature detected in earlier phase → must be removed → document in specification refinement

- **Architecture Evolution**: Architecture changes are ALLOWED only through:
  - Specification amendment
  - Plan revision with ADR documentation
  - Explicit user approval

- **Technology Stack**: Stack additions can only occur through:
  - Constitutional amendment
  - Phase specification update
  - User approval

### 3.3 Cross-Phase Dependencies

- **Backward Compatibility**: Earlier phases must remain compatible with later phases
- **Database Migrations**: Schema changes documented in migration history
- **API Evolution**: Version strategy defined in specifications
- **Breaking Changes**: Require explicit documentation and phase coordination

---

## PART IV: TECHNOLOGY CONSTRAINTS (MANDATORY)

### 4.1 Backend Stack (All Phases)

| Component | Technology | Notes |
|-----------|-----------|-------|
| Language | Python 3.10+ | Mandatory for all backend services |
| Framework | FastAPI | REST API framework of choice |
| ORM | SQLModel | Type-safe database models |
| Database | Neon PostgreSQL | Production-grade relational database |
| Package Manager | pip/poetry | Python dependency management |

### 4.2 Frontend Stack (Phase II+)

| Component | Technology | Notes |
|-----------|-----------|-------|
| Framework | Next.js 14+ | React-based SSR/SSG framework |
| Language | TypeScript | Strict typing required |
| Styling | CSS Modules / Tailwind | Component-scoped styles |
| State Management | React Hooks + Context | Minimal; Redux only if spec-approved |
| HTTP Client | fetch / axios | Standard HTTP communication |

### 4.3 Messaging & Real-Time (Phase III+)

| Component | Technology | Notes |
|-----------|-----------|-------|
| Message Broker | Apache Kafka | Event streaming for real-time features |
| WebSockets | FastAPI WebSocket | Real-time bidirectional communication |
| Caching | Redis | (Optional; use only if spec-approved) |

### 4.4 AI & Agents (Phase IV+)

| Component | Technology | Notes |
|-----------|-----------|-------|
| AI Framework | OpenAI Agents SDK | Agent orchestration and LLM integration |
| LLM Provider | OpenAI GPT-4+ | Primary language model |
| MCP Servers | Custom MCP Servers | Tool bridging and integrations |
| Vector DB | (TBD in spec) | For embeddings/search (if needed) |

### 4.5 Cloud-Native (Phase V+)

| Component | Technology | Notes |
|-----------|-----------|-------|
| Container Runtime | Docker | Container image building and execution |
| Orchestration | Kubernetes | Container orchestration platform |
| Service Mesh | Dapr | Distributed application runtime |
| Observability | (TBD in spec) | Logging, metrics, tracing |
| Message Queue | Kafka | Maintained from Phase III+ |

### 4.6 Technology Substitution Rules

- **NO substitutions without constitutional amendment**
- Exceptions for drop-in replacements (e.g., pytest → unittest with explicit justification)
- All substitution requests must be documented in ADR
- Phase constraints cannot be violated

---

## PART V: QUALITY PRINCIPLES

### 5.1 Clean Architecture (Mandatory)

```
Domain Layer (Entities, Use Cases)
    ↓
Application Layer (Services, DTOs)
    ↓
Interface Layer (Controllers, Presenters)
    ↓
Infrastructure Layer (Repositories, External Services)
```

All code must follow this layering:

- **Domain Logic**: Database-agnostic, framework-agnostic
- **Application Services**: Orchestrate domain logic, coordinate requests
- **Controllers/Routes**: HTTP routing, request/response handling
- **Infrastructure**: Database queries, external API calls, file I/O

### 5.2 Separation of Concerns (Mandatory)

- **One responsibility per class/function**
- **Database knowledge stays in repositories**
- **Business logic isolated from HTTP/presentation logic**
- **Tests can run without external dependencies (except database)**

### 5.3 Stateless Services (Where Required)

- **API endpoints**: Stateless HTTP handlers
- **Message processors**: Stateless event handlers
- **Agent services**: Stateless decision-making (state stored externally)
- **Exceptions**: Documented in specification with justification

### 5.4 Test-First Development (Non-Negotiable)

1. **Unit Tests**: Single responsibility verification
2. **Integration Tests**: API contract verification
3. **End-to-End Tests**: User workflow verification (Phase II+)
4. **Coverage**: Minimum 80% code coverage per module

Test execution:
- Tests written and approved before implementation
- Tests fail initially (Red phase)
- Code implemented to pass tests (Green phase)
- Refactoring occurs only with passing tests (Refactor phase)

### 5.5 Clear Error Handling

- **Typed exceptions**: Domain-specific error classes
- **Error propagation**: Errors flow up with context
- **HTTP status codes**: Correct 4xx/5xx codes per REST conventions
- **Error messages**: User-friendly, never exposing internals

### 5.6 Cloud-Native Readiness (All Phases)

All code must be deployable to:
- Containerized environments (Docker)
- Stateless execution models
- Configuration via environment variables
- Health checks and graceful shutdown
- Structured logging (JSON)

---

## PART VI: DEVELOPMENT WORKFLOW

### 6.1 Specification Phase

1. User defines requirements in specification document
2. Specification includes:
   - Problem statement
   - Acceptance criteria
   - Constraints and scope boundaries
   - Mock API contracts (if applicable)
3. User approval: ✅ Specification accepted
4. Agent prepares for planning phase

### 6.2 Planning Phase

1. Agent creates architecture plan (`.specify/specs/<feature>/plan.md`)
2. Plan includes:
   - High-level design decisions
   - Data model (if applicable)
   - API contracts (for backend)
   - Component architecture (for frontend)
   - Risk assessment and mitigation
3. Plan suggests ADRs for significant decisions
4. User approval: ✅ Plan accepted
5. Agent prepares task breakdown

### 6.3 Task Breakdown Phase

1. Agent creates tasks document (`.specify/specs/<feature>/tasks.md`)
2. Tasks include:
   - Testable success criteria
   - Implementation steps
   - File locations and scope
   - Phase assignment
3. User approval: ✅ Tasks accepted
4. Agent begins Red phase (test writing)

### 6.4 Red-Green-Refactor Cycle

#### Red Phase: Write Failing Tests
- Tests written to specification
- Tests fail (no implementation yet)
- Tests documented in tasks

#### Green Phase: Minimal Implementation
- Code written to pass tests
- No feature creep
- References spec and task
- Commits tie to tasks

#### Refactor Phase
- Code optimization within passing tests
- No new features
- No scope expansion
- Test coverage maintained

### 6.5 Code Review & Approval

- Specification compliance verification
- Test coverage verification (minimum 80%)
- Architecture adherence verification
- Code references to spec/tasks

---

## PART VII: PROMPT HISTORY RECORDS (PHRs)

All user interactions must be recorded in Prompt History Records:

### 7.1 PHR Structure

Location: `history/prompts/<category>/<ID>-<slug>.<stage>.prompt.md`

Categories:
- `constitution/` — Constitutional amendments and governance
- `<feature-name>/` — Feature-specific work (spec, plan, tasks, red, green, refactor)
- `general/` — General inquiries and exploration

### 7.2 PHR Mandatory Fields

```yaml
---
ID: <auto-incrementing>
TITLE: <3-7 words>
STAGE: <constitution|spec|plan|tasks|red|green|refactor|general>
DATE: <YYYY-MM-DD>
SURFACE: agent
MODEL: <claude-haiku-4-5-20251001|claude-sonnet-4-20250514|etc>
FEATURE: <feature-name-or-none>
BRANCH: <git-branch>
USER: <username>
COMMAND: <sp.* command or user query>
LABELS: [label1, label2, ...]
---

## Prompt

[Full user request, verbatim]

## Response

[Key agent output or artifacts created]

## Outcome

[Summary of acceptance, approvals, next steps]
```

### 7.3 PHR Creation Rules

- PHR created AFTER work completes (not during)
- All placeholders resolved (no `{{TEMPLATE}}` markers)
- Full user prompt preserved (not truncated)
- Key outputs summarized concisely

---

## PART VIII: ARCHITECTURAL DECISION RECORDS (ADRs)

Significant architectural decisions must be documented in ADRs.

### 8.1 ADR Triggers

An ADR is required when:

1. **Long-term consequence**: Affects system for extended period
2. **Multiple options considered**: More than one viable approach evaluated
3. **Cross-cutting**: Influences multiple components/phases

### 8.2 ADR Structure

Location: `history/adr/<title>.md`

```markdown
# <Decision Title>

## Status: Proposed | Accepted | Deprecated | Superseded

## Context
[What triggered this decision? What problem are we solving?]

## Decision
[What we decided to do and why]

## Rationale
[Why this option over others?]

## Alternatives Considered
[Other viable options and why we rejected them]

## Consequences
[What will change as a result of this decision?]

## Phase Introduced
[Which phase introduced this decision]

## Related Specs/PRs
[Links to relevant specifications and pull requests]
```

### 8.3 ADR Approval

- ADRs are suggested by agents
- ADRs are approved by users
- ADRs are NEVER auto-created
- ADRs become part of constitutional guidance

---

## PART IX: GOVERNANCE & ENFORCEMENT

### 9.1 Constitutional Supremacy

This Constitution supersedes:
- All phase specifications
- All implementation plans
- All task breakdowns
- All architectural decisions
- All code review guidelines

In case of conflict, the Constitution wins. Always.

### 9.2 Amendment Process

Constitutional amendments require:

1. **Identified Need**
   - Current constitution has a gap
   - Gap prevents necessary work
   - Gap is significant (not a clarification)

2. **Amendment Proposal**
   - Written change to constitution
   - Rationale for the amendment
   - Scope of impact

3. **User Approval**
   - User reviews proposed amendment
   - User approves or rejects
   - Approval is documented

4. **PHR Documentation**
   - Amendment recorded in PHR (stage: `constitution`)
   - Amendment date recorded
   - Previous version archived

### 9.3 Compliance Verification

Every agent action must verify:

- [ ] Current task aligns with approved specification
- [ ] Specification aligns with constitution
- [ ] Technology stack complies with Part IV
- [ ] Quality standards met (Part V)
- [ ] Development workflow followed (Part VI)
- [ ] No phase boundaries violated
- [ ] No feature invention or scope creep

Non-compliance triggers:
- Work pauses
- Specification refinement
- User notification and approval
- Compliance re-verification
- Work resumes

### 9.4 Conflict Resolution

When conflicts arise:

1. **Constitution vs. Specification**: Constitution wins → amend specification
2. **Specification vs. Code**: Specification wins → change code
3. **Code vs. Tests**: Tests win → change code
4. **Agent Uncertainty**: User is the resolver

---

## PART X: EXECUTION GUARANTEES

### 10.1 Agent Commitments

- **Specification First**: No code without approved spec
- **Precision**: Minimal diffs, exact spec compliance
- **Transparency**: All decisions documented in PHRs/ADRs
- **Compliance**: Constitution adherence verified before each change
- **Traceability**: Every code change references spec/task

### 10.2 User Commitments

- **Specification Authority**: Users define requirements
- **Timely Approval**: Specs/plans/tasks approved before work proceeds
- **Amendment Authority**: Users approve constitutional changes
- **Feedback**: Users provide actionable feedback on artifacts

### 10.3 Success Criteria

Implementation is successful when:

- ✅ All tests pass
- ✅ Code matches specification exactly
- ✅ No feature invention or scope creep
- ✅ Clean architecture maintained
- ✅ All changes documented in PHRs
- ✅ All significant decisions documented in ADRs
- ✅ Phase boundaries respected
- ✅ Technology stack adhered to
- ✅ Quality principles applied

---

## PART XI: QUICK REFERENCE CHECKLIST

Use this checklist before EVERY implementation task:

### Pre-Implementation Verification
- [ ] Task has approved specification
- [ ] Specification includes acceptance criteria
- [ ] Architecture plan exists and is approved
- [ ] Task breakdown is approved
- [ ] Task assignment is in correct phase
- [ ] Technology stack is constitutional
- [ ] No phase boundary violations detected
- [ ] Tests are written first (Red phase)

### During Implementation (Green-Refactor Cycle)
- [ ] Code implementation follows plan exactly
- [ ] No features added beyond specification
- [ ] All tests passing
- [ ] Code references specification and tasks
- [ ] Error handling matches spec
- [ ] Database layer isolated
- [ ] Clean architecture maintained
- [ ] Minimal code changes

### Post-Implementation Verification
- [ ] All tests passing (minimum 80% coverage)
- [ ] Code matches specification exactly
- [ ] PHR created and complete
- [ ] ADRs documented for significant decisions
- [ ] Phase boundaries maintained
- [ ] Technology stack compliant
- [ ] Quality principles applied
- [ ] Ready for user approval

---

## APPENDIX A: Glossary

| Term | Definition |
|------|-----------|
| **Spec** | Specification document defining WHAT to build |
| **Plan** | Architecture document defining HOW to build it |
| **Tasks** | Testable, approved work items |
| **Red-Green-Refactor** | TDD cycle: failing tests → implementation → optimization |
| **PHR** | Prompt History Record documenting user interactions |
| **ADR** | Architecture Decision Record for significant decisions |
| **Phase Boundary** | Strict separation between sequential phases |
| **Constitutional Compliance** | Adherence to this Constitution |
| **Feature Invention** | Adding features not in approved specification (FORBIDDEN) |
| **Spec-Driven Development** | Development guided by approved specifications |

---

## APPENDIX B: Phase Technology Matrix

| Technology | Phase I | Phase II | Phase III | Phase IV | Phase V |
|-----------|---------|---------|----------|---------|---------|
| Python | ✅ | ✅ | ✅ | ✅ | ✅ |
| FastAPI | ✅ | ✅ | ✅ | ✅ | ✅ |
| SQLModel | ✅ | ✅ | ✅ | ✅ | ✅ |
| PostgreSQL | ✅ | ✅ | ✅ | ✅ | ✅ |
| Next.js | ❌ | ✅ | ✅ | ✅ | ✅ |
| TypeScript | ❌ | ✅ | ✅ | ✅ | ✅ |
| Kafka | ❌ | ❌ | ✅ | ✅ | ✅ |
| WebSockets | ❌ | ❌ | ✅ | ✅ | ✅ |
| OpenAI SDK | ❌ | ❌ | ❌ | ✅ | ✅ |
| MCP Servers | ❌ | ❌ | ❌ | ✅ | ✅ |
| Docker | ❌ | ❌ | ❌ | ❌ | ✅ |
| Kubernetes | ❌ | ❌ | ❌ | ❌ | ✅ |
| Dapr | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## APPENDIX C: File Structure

```
.
├── .specify/
│   ├── memory/
│   │   ├── EVOLUTION_CONSTITUTION.md (THIS FILE)
│   │   └── constitution.md (legacy)
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   ├── adr-template.md
│   │   └── phr-template.prompt.md
│   ├── scripts/
│   │   └── bash/
│   │       └── create-phr.sh
│   └── commands/
│       ├── sp.constitution.md
│       ├── sp.specify.md
│       ├── sp.plan.md
│       ├── sp.tasks.md
│       ├── sp.implement.md
│       ├── sp.adr.md
│       └── ... (other commands)
│
├── specs/
│   ├── phase-1-core-api/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── phase-2-frontend-integration/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── ... (Phase III, IV, V similarly)
│   └── README.md (phase index)
│
├── history/
│   ├── prompts/
│   │   ├── constitution/
│   │   ├── phase-1-core-api/
│   │   ├── phase-2-frontend-integration/
│   │   ├── ... (Phase III, IV, V similarly)
│   │   └── general/
│   └── adr/
│       ├── decision-001-...md
│       ├── decision-002-...md
│       └── ... (numbered chronologically)
│
├── backend/
│   ├── app/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── interfaces/
│   │   └── infrastructure/
│   ├── tests/
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ... (Next.js structure)
│   ├── tests/
│   └── package.json
│
└── README.md (project overview)
```

---

**Constitutional Signature**

```
Document: Evolution of Todo - Global Constitution
Version: 1.0.0
Status: ACTIVE - Ratified 2025-12-30
Authority: Supreme governing document for all phases
Enforcement: Mandatory for all agents
Amendment Process: User approval required
Next Review: Post-Phase V completion
```

This Constitution is binding on all agents, specifications, plans, and implementations within the "Evolution of Todo" project. No work may proceed without explicit alignment to this document.

---

**End of Constitution**
