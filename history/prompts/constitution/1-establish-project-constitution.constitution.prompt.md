---
id: 1
title: Establish Project Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: gemini-pro
feature: none
branch: {{BRANCH}}
user: {{USER}}
command: /sp.constitution
labels: [constitution]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  []
---

## Prompt

/sp.constitution 
Project: Physical AI & Humanoid Robotics — A Docusaurus Textbook

Core principles:
- High technical accuracy (ROS 2, Gazebo, Unity, Isaac, VLA).
- Educational clarity for students learning Physical AI for the first time.
- Fully Docusaurus-compatible Markdown output (frontmatter + sidebars).
- Code should be runnable (Python, rclpy, ROS 2 launch files).
- Visual diagrams described with alt text.

Key standards:
- Each chapter: 1500–3000 words.
- Use modular, lecture-like structure: concepts → examples → code → exercises.
- Include 3+ exercises per chapter (hands-on, coding, conceptual).
- All chapters visible in sidebar and homepage links.
- Book title replaces Docusaurus default title.
- Remove default Docusaurus welcome page.

Constraints:
- 6–8 chapters total based on 4 core modules.
- Homepage must act as the "landing page" linking to all chapters.
- No copyrighted text > 25 consecutive words.
- Content must be student-friendly but technically rigorous.

Success criteria:
- Docusaurus website runs locally without errors.
- Homepage shows book title + links to all chapters.
- GitHub Pages deployment ready (clean structure).
- All chapters generated in Markdown with proper frontmatter.

## Response snapshot

Updated the project constitution in `.specify/memory/constitution.md` and the associated `plan-template.md`. The new constitution version is 1.0.0. A summary of the changes has been added as a comment to the top of the constitution file.

## Outcome

- ✅ Impact: Established the project constitution, providing a set of guiding principles and standards for the project.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - Modified: `.specify/memory/constitution.md`
  - Modified: `.specify/templates/plan-template.md`
- 🔁 Next prompts: The user can now proceed with other commands, knowing that the project has a clear constitution.
- 🧠 Reflection: The process of creating the constitution and updating the templates went smoothly. The manual creation of the PHR was necessary due to issues with the script.
