# AI-103 Mock Exam Simulator

> **Free, open-source exam simulator for Microsoft AI-103: Azure AI Apps and Agents Developer Associate**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Questions](https://img.shields.io/badge/Questions-1000%2B-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
[![Exam](https://img.shields.io/badge/Exam-AI--103-purple.svg)]()

---

## 🎯 What is this?

A **fully offline, browser-based mock exam simulator** for the **Microsoft AI-103 certification exam** — *Azure AI Apps and Agents Developer Associate*. Load your own JSON question bank, configure your exam settings, and practise in conditions that mirror the real exam.

No backend. No login. No data collection. Everything runs locally in your browser from a single HTML file.

---

## ✨ Features

- 📂 **Upload any JSON question bank** — load your own questions, swap banks anytime
- ⏱️ **Configurable timer** — 20 min / 40 min / 60 min / 130 min (real exam) / no timer
- ⏰ **Overtime tracking** — timer continues past zero with `+mm:ss` so you always finish
- 📊 **Live progressive stats bar** — correct / wrong / remaining / % / score out of 1000 (updates after every answer)
- 🔀 **Randomized question order** and **randomized drag-and-drop** item/slot positions
- 🗂️ **Question navigation grid** — jump to any question, colour-coded by result
- 💡 **Instant explanations** — correct answer stated first, then full reasoning
- 📋 **All real exam question types**:
  - Multiple choice (MCQ)
  - Select TWO
  - Code — complete the blank (Python)
  - Code — spot the bug (Python)
  - Drag and drop (match / order)
- 🎓 **Scenario-based question sets** — one scenario followed by a series of related questions, matching the real AI-103 exam format
- 📈 **Score out of 1000** — progressive scoring based on questions attempted (matches real Microsoft exam scaling)
- 🔁 **Review mode** — review all answers with explanations after completing the exam
- 🚀 **Zero dependencies** — single HTML file, works fully offline

---

## 🚀 Quick Start

### Option 1 — Download and open locally

1. Download `simulator.html`
2. Open it in any modern browser (Chrome, Edge, Firefox, Safari)
3. Upload a question bank JSON file
4. Configure your exam settings and start

### Option 2 — Use directly via GitHub Pages

Visit: `https://<your-username>.github.io/ai103-mock-exam/`

> No installation required.

---

## 📁 Repository Structure

```
ai103-mock-exam/
├── simulator.html          # The complete exam simulator (single file)
├── questions/
│   └── ai103_questions.json  # Official question bank (1000+ questions)
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 📋 Question Bank JSON Schema

Anyone can contribute questions. Each question must follow this exact schema:

```json
[
  {
    "tag": "f",
    "type": "mcq",
    "multi": false,
    "scen": null,
    "scenlabel": null,
    "text": "Question text goes here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": [0],
    "expl": "Correct answer: A — Option A.\n\nExplanation of why A is correct and why B, C, D are wrong."
  }
]
```

### Field reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | ✅ | Topic tag: `f` (Foundry/Agents), `s` (Scenario), `r` (Responsible AI), `c` (Content Understanding) |
| `type` | string | ✅ | Question type: `mcq`, `code`, `dragdrop` |
| `multi` | boolean | ✅ | `true` = Select TWO question, `false` = single answer |
| `scen` | string \| null | ✅ | Scenario text displayed above the question, or `null` |
| `scenlabel` | string \| null | ❌ | Optional label for the scenario block (e.g. `"Scenario 1 (Q1–Q7) — Healthcare AI"`) |
| `text` | string | ✅ | The question text |
| `options` | string[] | ✅ | Array of answer option strings (4 options recommended) |
| `answer` | number[] | ✅ | Array of correct option indices (0-based). Single: `[0]`. Select TWO: `[0, 2]` |
| `expl` | string | ✅ | Explanation. Must start with `"Correct answer: X — ..."` then `\n\n` then the explanation body |

### Additional fields for `code` questions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | ✅ | Code snippet. Use `___` (3+ underscores) for blanks in `complete` type |
| `codetype` | string | ✅ | `"complete"` (fill the blank) or `"bug"` (spot the error) |

### Additional fields for `dragdrop` questions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `items` | string[] | ✅ | The draggable items (left column) |
| `slots` | string[] | ✅ | The target slots (right column) |
| `correctMapping` | number[] | ✅ | `correctMapping[slotIndex] = itemIndex` that belongs in that slot |

### Example — MCQ question

```json
{
  "tag": "f",
  "type": "mcq",
  "multi": false,
  "scen": null,
  "text": "Which method on AIProjectClient initialises the client from a Foundry connection string?",
  "options": [
    "AIProjectClient.create()",
    "AIProjectClient.from_connection_string()",
    "AIProjectClient.connect()",
    "AIProjectClient.initialize()"
  ],
  "answer": [1],
  "expl": "Correct answer: B — AIProjectClient.from_connection_string().\n\nThe azure-ai-projects SDK uses from_connection_string() to instantiate the client. create(), connect(), and initialize() are not valid class methods."
}
```

### Example — Select TWO question

```json
{
  "tag": "r",
  "type": "mcq",
  "multi": true,
  "scen": null,
  "text": "Which TWO EU AI Act obligations apply to high-risk AI systems? (Select TWO)",
  "options": [
    "Conformity assessment before deployment",
    "Use of open-source models only",
    "Human oversight capability",
    "Deployment in EU regions only"
  ],
  "answer": [0, 2],
  "expl": "Correct answers: A and C.\n\nHigh-risk AI systems require conformity assessment before deployment (A) and human oversight capability (C). Open-source models are not required by the EU AI Act. EU region deployment is a GDPR consideration, not an EU AI Act requirement."
}
```

### Example — Code (complete the blank) question

```json
{
  "tag": "f",
  "type": "code",
  "codetype": "complete",
  "multi": false,
  "scen": null,
  "text": "Complete the blank to correctly create a message on an agent thread.",
  "code": "client.agents._____(  \n    thread_id=thread.id,\n    role=\"user\",\n    content=\"What is the refund policy?\"\n)",
  "options": [
    "add_message()",
    "send_message()",
    "create_message()",
    "post_message()"
  ],
  "answer": [2],
  "expl": "Correct answer: C — create_message().\n\nThe azure-ai-projects SDK uses create_message() to add messages to a thread. The other method names are not valid."
}
```

### Example — Drag and drop question

```json
{
  "tag": "f",
  "type": "dragdrop",
  "multi": false,
  "scen": null,
  "text": "Match each Foundry component to its primary function.",
  "items": ["Foundry Hub", "Foundry Project", "Prompt Flow", "Evaluation SDK"],
  "slots": [
    "Shared infrastructure layer — connections and security",
    "Developer workspace — models, agents, evaluations",
    "DAG-based LLM pipeline orchestration",
    "Quality and safety metric measurement"
  ],
  "correctMapping": [0, 1, 2, 3],
  "expl": "Correct matches: Hub → infrastructure | Project → workspace | Prompt Flow → pipeline | Evaluation SDK → quality metrics.\n\nThe Hub/Project hierarchy separates shared enterprise infrastructure from team workspaces. Prompt Flow orchestrates LLM pipelines. The Evaluation SDK measures groundedness, safety, coherence, and relevance."
}
```

### Example — Scenario question

```json
{
  "tag": "s",
  "type": "mcq",
  "multi": false,
  "scen": "A healthcare provider is building an AI-103 solution that processes patient voice recordings and clinical notes. The solution must transcribe calls, extract symptoms, and recommend a triage category. A clinician must approve all recommendations before they affect patient care.",
  "scenlabel": "Scenario 1 (Q1–Q5) — Healthcare Triage AI",
  "text": "Which Azure AI Speech feature should be used to process 5-minute phone call recordings asynchronously with speaker diarization?",
  "options": [
    "Real-time SpeechRecognizer with continuous recognition",
    "Batch transcription with diarization enabled via the Speech REST API",
    "ConversationTranscriber for real-time multi-speaker input",
    "SpeechRecognizer.recognize_once_async() in a loop"
  ],
  "answer": [1],
  "expl": "Correct answer: B — Batch transcription with diarization.\n\nBatch transcription handles long audio files asynchronously and supports speaker diarization. Real-time recognition is for live streams. ConversationTranscriber requires real-time input. recognize_once_async in a loop loses cross-segment context."
}
```

---

## 🏷️ Topic Tags

| Tag | Covers |
|-----|--------|
| `f` | Azure AI Foundry, Agents, Prompt Flow, Tracing, Evaluation, Deployments |
| `s` | Scenario-based questions (cross-service architecture) |
| `r` | Responsible AI, EU AI Act, GDPR, Microsoft RAI principles |
| `c` | Content Understanding, multimodal processing |

---

## 🎓 About the AI-103 Exam

| Detail | Info |
|--------|------|
| **Exam name** | Azure AI Apps and Agents Developer Associate |
| **Exam code** | AI-103 |
| **Certification** | Microsoft Certified: Azure AI Apps and Agents Developer Associate |
| **Passing score** | 700 / 1000 |
| **Exam duration** | 120 minutes |
| **Question types** | MCQ, Select TWO, drag-and-drop, case studies, code questions |
| **Replaces** | AI-102 (retired June 2026) |

### AI-103 Domain Weights

| Domain | Weight |
|--------|--------|
| Plan and manage an Azure AI solution | 25–30% |
| Implement generative AI and agentic solutions | 30–35% |
| Implement computer vision solutions | 10–15% |
| Implement text analysis solutions | 10–15% |
| Implement information extraction solutions | 10–15% |

---

## 🤝 Contributing

We welcome contributions of new questions, bug fixes, and improvements!

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

**Quick contribution guide:**
1. Fork the repository
2. Add your questions to `questions/ai103_questions.json` following the schema above
3. Validate your JSON is valid (use [jsonlint.com](https://jsonlint.com))
4. Ensure explanations start with `"Correct answer: X — ..."` format
5. Submit a pull request with a clear description of what you added

---

## ✅ Question Quality Guidelines

- All four options must be **plausible** — no obviously wrong distractors
- Wrong options must use **real Azure service names** applied incorrectly
- Scenario questions must have a **clear constraint** (cost, latency, compliance, no custom training) that determines the correct answer
- Code questions must use **current SDK method names** — no deprecated APIs
- Explanations must explain **why each wrong option is wrong**, not just why the correct one is right
- No questions about **deprecated services**: LUIS, QnA Maker, Text Analytics (use Azure AI Language), AI-102 (use AI-103)

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for full text.

Free to use, modify, and distribute. Attribution appreciated but not required.

---

## ⭐ Star this repo

If this simulator helped your exam preparation, please ⭐ star the repository — it helps others find it.

---

*Not affiliated with Microsoft. AI-103 is a trademark of Microsoft Corporation.*
