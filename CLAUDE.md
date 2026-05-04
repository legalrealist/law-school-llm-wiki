# Law School LLM Wiki — Schema & Workflows

This is the schema file for a law school knowledge wiki maintained by Claude Code. It defines the
directory layout, page conventions, and workflows that Claude follows to build
and maintain this wiki. Read this file at the start of every session.

---

## Domain Configuration

> **Edit this section to match your subject matter.**
> The defaults below are for legal research. Replace page types, directories,
> tags, and templates with whatever fits your domain.

**Domain**: Legal Research
**Page types**: course, doctrine, case, statute, overview
**Tag conventions**: subject area keywords (e.g. `[contracts, offer-acceptance]`)

---

## Directory Layout

```
law-school-llm-wiki/
├── CLAUDE.md                  ← this file (schema & instructions)
├── raw/                       ← IMMUTABLE source documents — read only, never modify
│   ├── extracted/             ← pre-extracted .txt versions of all sources (READ HERE FIRST)
│   ├── articles/              ← articles, reference pieces
│   ├── papers/                ← PDFs, reports, academic papers
│   ├── notes/                 ← primary source documents (.docx, .pdf)
│   └── assets/                ← images and attachments
└── wiki/                      ← Claude-owned — Claude writes and maintains everything here
    ├── index.md               ← master catalog of all wiki pages (update on every ingest)
    ├── log.md                 ← append-only chronological record of operations
    ├── overview.md            ← evolving synthesis across all subjects
    ├── courses/               ← one page per course or topic area
    ├── doctrines/             ← one page per core concept or rule
    ├── cases/                 ← one page per important case or example
    └── statutes/              ← one page per statute, regulation, or formal reference
```

> **Adapting the structure:** Rename the directories under `wiki/` to match your
> page types. For a software engineering wiki you might use `concepts/`,
> `patterns/`, `libraries/`. For medical research: `conditions/`, `treatments/`,
> `studies/`. The workflows below reference these generically — just keep the
> names consistent with your page types.

**Rule**: Never modify anything under `raw/` — **except `raw/extracted/`**, where
Claude saves extracted text on first ingest. Original source files in `raw/notes/`,
`raw/articles/`, and `raw/papers/` are immutable. All wiki content lives under `wiki/`.

---

## Page Conventions

### Frontmatter (YAML, Dataview-compatible)

Every wiki page must start with frontmatter:

```yaml
---
type: course | doctrine | case | statute | overview
tags: [tag1, tag2]
sources: 0
updated: YYYY-MM-DD
---
```

- `type`: one of your defined page types (edit to match your domain)
- `tags`: subject area keywords
- `sources`: count of raw sources that have contributed to this page
- `updated`: date this page was last modified (ISO format)

### Cross-references

Always use Obsidian wikilinks: `[[Page Name]]`. File names should match the
page title exactly.

### Filenames

Use the page's full title exactly, with spaces and natural capitalization:
`Consideration.md`, `Hadley v Baxendale.md`, `Contracts I.md`. The filename
must match the H1 heading, which must match the `[[wikilink]]` used to
reference the page. This is what makes Obsidian backlinks work.

---

## Page Templates

> **Edit these templates to match your domain.** Each page type should have
> a defined structure so pages are consistent and comparable.

### Course Pages

Each course page should include:
- Course info (professor, semester, year)
- High-level outline of topics covered
- Key doctrines taught (wikilinked to doctrine pages)
- Key cases covered (wikilinked to case pages)
- Exam approach / checklist if present in the notes

### Doctrine Pages

Each doctrine page should include:
- Definition / rule statement
- Elements (numbered list)
- Exceptions and edge cases
- Policy rationale
- Key cases illustrating the doctrine (wikilinked)
- Which courses cover this (wikilinked)

### Case Pages

Each case page should include:
- Citation and court
- Facts (brief)
- Issue
- Holding
- Rule / doctrine it stands for
- Significance / why it matters
- Which courses reference it (wikilinked)

### Statute / Reference Pages

Each reference page should include:
- Full citation or identifier
- Summary of content
- Key provisions or sections
- Related doctrines (wikilinked)
- Which courses reference it (wikilinked)

---

## Ingest Workflow

When the user asks Claude to ingest a source from `raw/`:

0. **Check `wiki/log.md` first.** If an `ingest-complete` entry already exists
   for this source path, tell the user it's already been ingested and ask if
   they want to re-ingest (which will update existing pages with a fresh read).
   If an `ingest-start` exists without a matching `ingest-complete`, the previous
   ingest was interrupted — resume from where it left off.
1. **Read** the source. **Always check `raw/extracted/` first** — pre-extracted
   `.txt` versions are stored there and are much faster to read. If no `.txt`
   counterpart exists, read the original file and **save the extracted text
   to `raw/extracted/<filename>.txt`** so future ingests are faster.
   Write `ingest-start` to `wiki/log.md` before doing anything else.
2. **Discuss** key takeaways with the user if they want — what subjects are
   covered, what concepts are central.
3. **Write or update `wiki/courses/<slug>.md`** — a course summary page.
4. **Update doctrine pages** — for each significant doctrine in the source:
   open `wiki/doctrines/<slug>.md` (create if missing), integrate definitions,
   elements, exceptions, and cases.
5. **Update case pages** — for significant cases cited:
   open `wiki/cases/<slug>.md` (create if missing), fill in
   facts/holding/rule.
6. **Update `wiki/overview.md`** if the source adds a new subject area or
   meaningfully changes the synthesis.
7. **Update `wiki/index.md`** — add newly created pages to the catalog.
8. **Write `ingest-complete` to `wiki/log.md`** — include the `Source:` path
   and list of all pages updated.

### Reading sources — order of preference

1. **`raw/extracted/<filename>.txt`** — use the Read tool directly. Fast and preferred.
2. **`raw/notes/<filename>.pdf`** — use the Read tool with `pages` parameter
   if no `.txt` exists. After reading, save extracted text to
   `raw/extracted/<filename>.txt` for next time.
3. **`raw/notes/<filename>.docx`** — use python-docx as a last resort:

```python
from docx import Document
doc = Document('raw/notes/filename.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
print(text)
# Save to raw/extracted/ for future ingests
with open('raw/extracted/filename.txt', 'w') as f:
    f.write(text)
```

The `raw/extracted/` directory mirrors `raw/notes/` with the same base filenames
(`.docx` → `.txt`, `.pdf` → `.txt`). Claude creates these automatically on
first ingest if they don't exist.

---

## Query Workflow

When the user asks a question:

1. Read `wiki/index.md` to identify relevant pages.
2. Read those pages and follow wikilinks as needed.
3. Synthesize an answer with citations to wiki pages.
4. **If the answer is substantive** (e.g. a comparison, a synthesis), offer
   to file it as a new wiki page.

---

## Lint Workflow

Periodically, or when asked:

1. **Orphan pages** — pages with no inbound links.
2. **Missing pages** — wikilinks pointing to pages that don't exist yet.
3. **Contradictions** — conflicting statements across sources
   (flag with `> [!warning]`).
4. **Incomplete pages** — pages missing key template sections.
5. **Missing cross-references** — pages that should link to each other but don't.

---

## Index Format

`wiki/index.md` uses per-section markdown tables:

```markdown
| Page | Summary | Updated |
|------|---------|---------|
| [[Page Name]] | One-line summary | YYYY-MM-DD |
```

One section per page type (e.g. Overview, Courses, Doctrines, Cases, Statutes).

---

## Log Format

All log entries use the format:

```
## [YYYY-MM-DD HH:MM] <operation> | <title>
```

Operations: `ingest-start`, `ingest-complete`, `query`, `lint`, `update`, `init`.

### Ingest entries (two entries per source)

Write `ingest-start` at the **beginning** of every ingest — before writing
any wiki pages:

```
## [YYYY-MM-DD HH:MM] ingest-start | Topic Name
Source: raw/extracted/filename.txt
```

Write `ingest-complete` at the **end**, after all pages are written:

```
## [YYYY-MM-DD HH:MM] ingest-complete | Topic Name
Source: raw/extracted/filename.txt
Pages updated: [[Page 1]], [[Page 2]], [[Page 3]]
```

The `Source:` line must be the exact relative path from the project root.
The log uses `ingest-complete` + `Source:` to detect which files have been
processed. If a session ends before writing `ingest-complete`, the source
will appear as in-progress on the next run.

Entries are append-only — never delete or edit past entries.

---

## Notes

- **Prefer updating existing doctrine pages** over creating new ones. Many
  courses cover the same doctrines — build up one authoritative page per
  doctrine rather than duplicating across courses.
- **Exam checklists are gold.** If a source has an issue-spotting checklist
  or exam approach, extract it prominently into the course page and the
  relevant doctrine pages.
- **Cross-course connections matter.** When a doctrine appears in multiple
  courses (e.g. consideration in Contracts I and II), note the cross-reference
  on the doctrine page.
