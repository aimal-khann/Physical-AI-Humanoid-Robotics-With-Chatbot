<!--
Sync Impact Report:
Version change: 1.0.0 (old) -> 1.1.0 (new)
Modified principles:
  - Added: VI. AI Fidelity & Safety
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/sp.adr.toml: ✅ updated
  - .specify/templates/commands/sp.analyze.toml: ✅ updated
  - .specify/templates/commands/sp.checklist.toml: ✅ updated
  - .specify/templates/commands/sp.clarify.toml: ✅ updated
  - .specify/templates/commands/sp.constitution.toml: ✅ updated
  - .specify/templates/commands/sp.git.commit_pr.toml: ✅ updated
  - .specify/templates/commands/sp.implement.toml: ✅ updated
  - .specify/templates/templates/commands/sp.phr.toml: ✅ updated
  - .specify/templates/commands/sp.plan.toml: ✅ updated
  - .specify/templates/commands/sp.specify.toml: ✅ updated
  - .specify/templates/commands/sp.tasks.toml: ✅ updated
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics — A Docusaurus Textbook Constitution

## Core Principles

### I. High Technical Accuracy
High technical accuracy (ROS 2, Gazebo, Unity, Isaac, VLA).

### II. Educational Clarity
Educational clarity for students learning Physical AI for the first time.

### III. Docusaurus Compatibility
Fully Docusaurus-compatible Markdown output (frontmatter + sidebars).

### IV. Runnable Code
Code should be runnable (Python, rclpy, ROS 2 launch files).

### V. Visual Accessibility
Visual diagrams described with alt text.

### VI. AI Fidelity & Safety
The AI chatbot must strictly adhere to the 'Retrieval-Augmented Generation' (RAG) pattern. It must ONLY answer questions using content retrieved from the textbook. If the answer is not in the book, it must explicitly state that it does not know, rather than fabricating information.

## Key Standards

- Each chapter: 1500–3000 words.
- Use modular, lecture-like structure: concepts → examples → code → exercises.
- Include 3+ exercises per chapter (hands-on, coding, conceptual).
- All chapters visible in sidebar and homepage links.
- Book title replaces Docusaurus default title.
- Remove default Docusaurus welcome page.

## Constraints

- 6–8 chapters total based on 4 core modules.
- Homepage must act as the "landing page" linking to all chapters.
- No copyrighted text > 25 consecutive words.
- Content must be student-friendly but technically rigorous.

## Governance

All development must adhere to the following success criteria:
- Docusaurus website runs locally without errors.
- Homepage shows book title + links to all chapters.
- GitHub Pages deployment ready (clean structure).
- All chapters generated in Markdown with proper frontmatter.

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-07