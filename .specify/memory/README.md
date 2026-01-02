# Constitutional Governance Framework

**Evolution of Todo Project - Master Documentation Index**

---

## Overview

This directory contains the constitutional and governance documents for the Evolution of Todo project. These documents establish mandatory principles, agent behavior rules, phase governance, and quality standards that govern all development work across Phase I through Phase V.

**Status**: ✅ Complete and ratified
**Version**: 1.0.0
**Ratified**: 2025-12-30

---

## Core Documents

### 1. **EVOLUTION_CONSTITUTION.md** (Supreme Governing Document)

The authoritative constitutional framework for the entire project.

**Contents**:
- **Part I**: Spec-Driven Development (mandatory workflow)
- **Part II**: Agent Behavior Rules (forbidden/required actions)
- **Part III**: Phase Governance (five phases with strict boundaries)
- **Part IV**: Technology Constraints (phase-by-phase tech stack)
- **Part V**: Quality Principles (clean architecture, testing, etc.)
- **Part VI**: Development Workflow (spec → plan → tasks → implement)
- **Part VII**: Prompt History Records (PHR requirements)
- **Part VIII**: Architectural Decision Records (ADR requirements)
- **Part IX**: Governance & Enforcement (constitutional amendments)
- **Part X**: Execution Guarantees (commitments and success criteria)
- **Part XI**: Quick Reference Checklist

**When to use**: Before any implementation work. This is the source of truth.

**Size**: ~850 lines | **Read time**: 30-45 minutes

---

### 2. **CONSTITUTION_USAGE_GUIDE.md** (Practical Implementation Guide)

How to apply the Constitution in daily development work.

**Contents**:
- Five-step workflow (Constitution → Spec → Plan → Tasks → Implement)
- Key rules to enforce (6 critical rules)
- Constitutional compliance checklist
- Common violations and fixes
- Phase reference table
- Amendment process
- Enforcement strategy
- Success indicators

**When to use**: When implementing features, unsure about allowed actions, or enforcing constitution.

**Size**: ~450 lines | **Read time**: 15-20 minutes

---

### 3. **AGENT_COMMAND_REFERENCE.md** (Quick Reference for Agents)

Concise command reference for agent implementation tasks.

**Contents**:
- Pre-task verification checklist
- Workflow commands (8 key steps)
- Agent do's and don'ts
- Decision tree for common questions
- File structure for new work
- Phase templates (5 phase examples)
- Common commands reference
- Compliance checklist
- Troubleshooting guide

**When to use**: Quick lookup during implementation. Pocket reference for agents.

**Size**: ~350 lines | **Read time**: 10-15 minutes

---

## Supporting Documents (Specifications)

### **specs/README.md** (Phase Index)

Master index linking all phase specifications to the Constitution.

**Contents**:
- Phase hierarchy overview
- Phase I-V scope definitions
- Acceptance criteria for each phase
- Technology stack matrix
- Phase creation template
- Next steps for Phase I

**When to use**: Planning new phases, understanding phase scope, checking phase dependencies.

---

## Work-Related Documents

### **history/prompts/** (Prompt History Records)

Records of all user interactions and agent work:

```
history/prompts/
├── constitution/          # Constitutional amendments
│   └── 001-evolution-todo-global-constitution.constitution.prompt.md
├── phase-1-core-api/     # Phase I work
├── phase-2-frontend-integration/  # Phase II work
├── phase-3-advanced-features/     # Phase III work
├── phase-4-ai-agents/             # Phase IV work
├── phase-5-cloud-native/          # Phase V work
└── general/              # General inquiries
```

**Purpose**: Audit trail of decisions, experiments, and approvals.

### **history/adr/** (Architectural Decision Records)

Records of significant architectural decisions:

```
history/adr/
├── decision-001-...md
├── decision-002-...md
└── ...
```

**Purpose**: Document rationale for long-term architectural choices.

---

## Document Relationships

```
┌─────────────────────────────────────────────────────────────┐
│  EVOLUTION_CONSTITUTION.md (Supreme Authority)              │
│  - Immutable governing framework                            │
│  - Non-negotiable principles                                │
│  - Phase boundaries and tech constraints                    │
└────────────┬──────────────────────────────────────────────┘
             │
             ├─→ CONSTITUTION_USAGE_GUIDE.md
             │   (How to apply the Constitution)
             │
             ├─→ AGENT_COMMAND_REFERENCE.md
             │   (Practical command reference)
             │
             ├─→ specs/README.md
             │   └─→ specs/phase-N/spec.md
             │   └─→ specs/phase-N/plan.md
             │   └─→ specs/phase-N/tasks.md
             │
             ├─→ history/prompts/
             │   (Records of all work)
             │
             └─→ history/adr/
                 (Architectural decisions)
```

---

## Quick Navigation

### I need to...

**Understand the Constitution**
→ Read: EVOLUTION_CONSTITUTION.md (all parts)

**Apply the Constitution to my work**
→ Read: CONSTITUTION_USAGE_GUIDE.md

**Find a quick command reference**
→ Read: AGENT_COMMAND_REFERENCE.md

**Create a new phase specification**
→ Read: specs/README.md

**Document my work**
→ Create: history/prompts/<phase>/<ID>-<slug>.<stage>.prompt.md

**Document a major architectural decision**
→ Create: history/adr/<decision-title>.md

**Check if something is allowed**
→ Check: EVOLUTION_CONSTITUTION.md Part II + Part IV

**Understand phase scope**
→ Check: specs/README.md or EVOLUTION_CONSTITUTION.md Part III

**Find previous work on this feature**
→ Check: history/prompts/<feature-name>/

**Amend the Constitution**
→ Propose → Document → Get approval → Update EVOLUTION_CONSTITUTION.md

---

## Reading Guide by Role

### For New Agents

1. Start: CONSTITUTION_USAGE_GUIDE.md (15 min)
2. Reference: AGENT_COMMAND_REFERENCE.md (during work)
3. Deep dive: EVOLUTION_CONSTITUTION.md (as needed)

**Total setup time**: ~1 hour

### For Users/Approvers

1. Start: EVOLUTION_CONSTITUTION.md (all parts, 45 min)
2. Reference: CONSTITUTION_USAGE_GUIDE.md (during reviews)
3. Check: specs/README.md (for phase scope)

**Total setup time**: ~1.5 hours

### For Architects

1. Start: EVOLUTION_CONSTITUTION.md (all parts, 45 min)
2. Focus: Part III (Phase Governance), Part V (Quality), Part VIII (ADRs)
3. Reference: specs/README.md for phase architecture

**Total setup time**: ~1 hour

---

## Constitutional Principles at a Glance

### The Immutable Workflow
```
Constitution → Specification → Plan → Tasks → Implementation
```
All code changes must align to this workflow.

### The Five Phases
| Phase | Focus | Tech Stack | Key Addition |
|-------|-------|-----------|--------------|
| I | Core API | Python, FastAPI, PostgreSQL | Foundation |
| II | Web UI | Next.js, TypeScript | Frontend |
| III | Real-Time | Kafka, WebSockets | Streaming |
| IV | AI Agents | OpenAI SDK, MCP | Intelligence |
| V | Cloud-Native | Docker, Kubernetes, Dapr | Enterprise |

### Non-Negotiable Rules
1. ✅ No code without approved spec
2. ✅ Spec drives code, not vice versa
3. ✅ No feature invention
4. ✅ Respect phase boundaries
5. ✅ Technology stack is fixed (Part IV)
6. ✅ Test-first development (Red-Green-Refactor)

### Quality Standards
- Clean architecture (domain/application/interface/infrastructure layers)
- Separation of concerns (one responsibility per class)
- Stateless services (state managed externally)
- Test coverage: Minimum 80%
- Cloud-native ready (containerizable, configurable, observable)

---

## Amendment Process

If the Constitution needs updating:

1. **Identify need**: Constitutional gap or ambiguity
2. **Propose change**: Document rationale and scope
3. **Get approval**: User reviews and approves
4. **Update document**: Edit EVOLUTION_CONSTITUTION.md
5. **Document amendment**: Create PHR with stage: `constitution`
6. **Resume work**: All agents follow updated Constitution

---

## File Locations Quick Reference

```
.specify/memory/              ← Constitutional documents (THIS DIRECTORY)
├── EVOLUTION_CONSTITUTION.md ← Supreme authority
├── CONSTITUTION_USAGE_GUIDE.md ← How-to guide
├── AGENT_COMMAND_REFERENCE.md ← Quick reference
└── README.md                 ← This file

specs/                        ← Phase specifications
├── README.md                 ← Phase index
├── phase-1-core-api/
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
└── phase-N/
    ├── spec.md
    ├── plan.md
    └── tasks.md

history/                      ← Work records
├── prompts/                  ← User interactions (PHRs)
│   ├── constitution/
│   ├── phase-N/
│   └── general/
└── adr/                      ← Architectural decisions
    ├── decision-001-*.md
    └── ...
```

---

## Constitutional Authority

**This Constitution:**
- Is the supreme governing document for all project work
- Supersedes all other guidelines, plans, and specifications
- Applies to all agents across all phases
- Cannot be circumvented or overridden
- May only be amended through explicit user approval

**No work may proceed without alignment to this Constitution.**

---

## Next Steps

### For Phase I Implementation

1. Read EVOLUTION_CONSTITUTION.md completely
2. Create specs/phase-1-core-api/spec.md
3. Get user approval
4. Create specs/phase-1-core-api/plan.md
5. Get user approval
6. Create specs/phase-1-core-api/tasks.md
7. Get user approval
8. Begin Red-Green-Refactor implementation cycle

### For All Future Work

- Every task starts with Constitution review
- Every implementation follows spec-first workflow
- Every significant decision gets an ADR
- Every work session creates a PHR
- Every line of code references its specification

---

## Document Versions

| Document | Version | Ratified | Status |
|----------|---------|----------|--------|
| EVOLUTION_CONSTITUTION.md | 1.0.0 | 2025-12-30 | Active |
| CONSTITUTION_USAGE_GUIDE.md | 1.0.0 | 2025-12-30 | Active |
| AGENT_COMMAND_REFERENCE.md | 1.0.0 | 2025-12-30 | Active |
| specs/README.md | 1.0.0 | 2025-12-30 | Active |

---

## Support & Questions

**Question**: "Is [action] allowed?"
**Answer**: Check EVOLUTION_CONSTITUTION.md Part II (Agent Behavior)

**Question**: "How do I implement [feature]?"
**Answer**: Check CONSTITUTION_USAGE_GUIDE.md or AGENT_COMMAND_REFERENCE.md

**Question**: "What's in [phase]?"
**Answer**: Check EVOLUTION_CONSTITUTION.md Part III or specs/README.md

**Question**: "Can I use [technology]?"
**Answer**: Check EVOLUTION_CONSTITUTION.md Part IV

**Question**: "How do I amend the Constitution?"
**Answer**: Check CONSTITUTION_USAGE_GUIDE.md section "When to Amend"

---

**Remember**: The Constitution is supreme. Follow it. Always.

---

**Document Created**: 2025-12-30
**Ratified By**: Constitutional Charter
**Authority**: Evolution of Todo Project
