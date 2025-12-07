---
id: 2
title: "Add AI Fidelity & Safety to Constitution"
stage: "constitution"
date: 2025-12-07
surface: "agent"
model: "gemini-1.5-flash"
feature: "none"
branch: "main"
user: "(unknown)"
command: "/sp.constitution Update the project constitution to add a new Core Principle regarding AI safety."
labels: ["constitution"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

## Prompt

```text
/sp.constitution Update the project constitution to add a new Core Principle regarding AI safety.

Add this specific principle to the "Core Principles" section:
"VI. AI Fidelity & Safety: The AI chatbot must strictly adhere to the 'Retrieval-Augmented Generation' (RAG) pattern. It must ONLY answer questions using content retrieved from the textbook. If the answer is not in the book, it must explicitly state that it does not know, rather than fabricating information."

Do not remove or alter any existing principles about the textbook structure or educational clarity. Keep the version history and simply increment the version number.
```

## Response

```text
The project constitution (`.specify/memory/constitution.md`) has been updated to version `0.1.0`. A new core principle, "VI. AI Fidelity & Safety," has been added, and the `Last Amended Date` has been set to `2025-12-07`. The file also includes a Sync Impact Report.
```

## Outcome

Successfully updated the project constitution and generated a Sync Impact Report.

## Evaluation
The user's request was to update the project constitution with a new principle and increment the version. This was successfully completed.