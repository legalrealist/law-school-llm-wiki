# Law School LLM Wiki

An AI-maintained law school knowledge base powered by [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview). Adapted from [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern for legal education.

Drop in your course outlines, case briefs, and class notes. Claude reads, extracts, and builds a structured, cross-referenced wiki — one authoritative page per doctrine, one per case — with Obsidian-compatible wikilinks throughout.

## The idea

Most people's experience with LLMs and documents is RAG: upload files, ask a question, the model retrieves chunks and generates an answer. Nothing accumulates. Ask a subtle question that requires synthesizing five outlines, and the LLM has to find and piece together fragments every time.

Karpathy's insight is to flip this: instead of querying raw documents, have the LLM **build a wiki first**. When you ingest a new source, the LLM reads it, extracts key concepts, creates or updates structured pages, and cross-references everything. Knowledge compounds. The wiki gets smarter with every source you feed it.

This repo applies that pattern to law school. Course outlines become course pages. Legal rules become doctrine pages with elements, exceptions, and policy rationale. Important cases get their own pages with facts, holdings, and significance. Everything links to everything else.

## Quick start

### 1. Clone or use this template

```bash
git clone https://github.com/YOUR_USERNAME/law-school-llm-wiki.git
cd law-school-llm-wiki
```

### 2. Add your source material

Drop your course outlines, case briefs, supplements, and notes into `raw/`:

```
raw/
├── notes/       ← course outlines, class notes (.pdf, .docx)
├── articles/    ← law review articles, secondary sources
├── papers/      ← case PDFs, statutes, supplements
└── assets/      ← images and attachments
```

### 3. Pre-extract text (recommended)

For faster ingestion, extract text versions and place them in `raw/extracted/`. Claude checks here first before parsing PDFs or Word docs.

```
raw/extracted/
├── Contracts_I_FL15.txt      ← from Contracts_I_FL15.docx
├── Torts_SP16.txt            ← from Torts_SP16.pdf
```

### 4. Open Claude Code

```bash
cd law-school-llm-wiki
claude
```

Claude reads `CLAUDE.md` automatically and understands the entire project.

### 5. Ingest a source

```
Ingest raw/notes/Contracts_I_FL15.docx
```

Claude will:
1. Read the source (checking `raw/extracted/` first)
2. Discuss key takeaways with you
3. Create or update the course page (`wiki/courses/Contracts I.md`)
4. Create or update doctrine pages (`wiki/doctrines/Consideration.md`, etc.)
5. Create or update case pages (`wiki/cases/Hadley v Baxendale.md`, etc.)
6. Update the master index and log

### 6. Query your wiki

```
What are the elements of promissory estoppel, and which courses cover it?
```

```
Compare the consideration doctrine across Contracts I and Contracts II.
```

```
Give me an exam checklist for a contracts issue spotter.
```

### 7. Lint for quality

```
Run a lint check on the wiki.
```

Finds orphan pages, broken wikilinks, conflicting rule statements across courses, and incomplete entries.

## What the wiki looks like

After ingesting a few course outlines, you'll have:

```
wiki/
├── index.md                          ← master catalog
├── log.md                            ← what's been ingested, when
├── overview.md                       ← synthesis across all subjects
├── courses/
│   ├── Contracts I.md                ← course summary + exam approach
│   ├── Torts.md
│   └── Civil Procedure.md
├── doctrines/
│   ├── Consideration.md              ← elements, exceptions, policy, cases
│   ├── Promissory Estoppel.md
│   ├── Negligence.md
│   └── Personal Jurisdiction.md
├── cases/
│   ├── Hadley v Baxendale.md         ← facts, holding, rule, significance
│   ├── Palsgraf v Long Island Railroad.md
│   └── International Shoe v Washington.md
└── statutes/
    ├── UCC Article 2.md
    └── FRCP Rule 12.md
```

Every page uses Obsidian `[[wikilinks]]`. Open the `wiki/` folder as an Obsidian vault and you get backlinks, graph view, and Dataview-compatible frontmatter for free.

## Adapting to other domains

The CLAUDE.md schema is written for law school but the pattern works for anything. To adapt:

1. Change the **page types** — replace `course | doctrine | case | statute` with your domain's categories
2. Change the **page templates** — each type has a defined structure in CLAUDE.md
3. Rename the **directories** under `wiki/` to match
4. Update the **frontmatter** schema

See the "Domain Configuration" section at the top of CLAUDE.md.

### Example adaptations

- **Medical school**: `course`, `condition`, `treatment`, `mechanism`, `drug`
- **Software engineering**: `project`, `concept`, `pattern`, `library`, `architecture`
- **Academic research**: `paper`, `concept`, `method`, `finding`, `researcher`
- **History**: `period`, `event`, `person`, `source`, `theme`

## Using with Obsidian

The wiki is fully Obsidian-compatible:

1. Open `wiki/` as an Obsidian vault
2. All `[[wikilinks]]` resolve correctly
3. Backlinks and graph view work out of the box
4. Frontmatter is Dataview-compatible for advanced queries
5. Filenames match page titles exactly (e.g., `Hadley v Baxendale.md`)

## How it works under the hood

### Three-layer architecture

Following Karpathy's pattern:

- **Sources** (`raw/`) — your immutable source documents. Never modified.
- **Wiki** (`wiki/`) — LLM-generated and maintained. Structured pages with cross-references.
- **Schema** (`CLAUDE.md`) — the rules that govern how Claude builds and maintains the wiki.

### Ingest workflow

When you add a source, Claude doesn't just index it. It reads, understands, and integrates it — updating existing doctrine pages, creating new case pages, noting contradictions, and strengthening cross-references. The log tracks what's been processed so nothing gets ingested twice.

### Persistence across sessions

No database. No vector store. Claude reads `wiki/log.md` at the start of each session to know what's been done. The wiki itself is the knowledge base. Plain markdown files are the persistence layer.

## Credits

Based on [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern (April 2026). Karpathy's insight: instead of querying raw documents every time (RAG), have the LLM build a structured, interlinked knowledge base that compounds with every source.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (CLI or Desktop)
- A paid Anthropic plan (Pro, Max, Team, or Enterprise)
- Your law school notes

## License

MIT
