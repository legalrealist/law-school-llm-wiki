# Claude Wiki — Schema & Workflows

This is the schema file for a Claude-maintained knowledge wiki. It defines the
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
claude-wiki/
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

**Rule**: Never modify anything under `raw/`. All wiki content lives under `wiki/`.

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

### Course / Topic Pages

Each course or topic page should include:
- Topic info (scope, context, timeframe)
- High-level outline of subtopics covered
- Key concepts taught (wikilinked to concept pages)
- Key examples or cases (wikilinked)
- Summary or checklist if present in the source

### Concept / Doctrine Pages

Each concept page should include:
- Definition / core statement
- Elements or components (numbered list)
- Exceptions and edge cases
- Rationale or motivation
- Key examples illustrating the concept (wikilinked)
- Which topics cover this (wikilinked)

### Case / Example Pages

Each case or example page should include:
- Source and attribution
- Context (brief)
- Key question or issue
- Answer or finding
- Rule or principle it demonstrates
- Significance / why it matters
- Which topics reference it (wikilinked)

### Statute / Reference Pages

Each reference page should include:
- Full citation or identifier
- Summary of content
- Key provisions or sections
- Related concepts (wikilinked)
- Which topics reference it (wikilinked)

---

## Ingest Workflow

When the user asks Claude to ingest a source from `raw/`:

1. **Read** the source. **Always check `raw/extracted/` first** — pre-extracted
   `.txt` versions are stored there and are much faster to read. Only fall back
   to PDF or Word parsing if no `.txt` counterpart exists.
   Write `ingest-start` to `wiki/log.md` before doing anything else.
2. **Discuss** key takeaways with the user if they want — what subjects are
   covered, what concepts are central.
3. **Write or update topic pages** — a summary page for the source's main topic.
4. **Update concept pages** — for each significant concept in the source:
   open the relevant page (create if missing), integrate definitions,
   components, exceptions, and examples.
5. **Update example/case pages** — for significant cases or examples cited:
   open the relevant page (create if missing), fill in the template fields.
6. **Update `wiki/overview.md`** if the source adds a new subject area or
   meaningfully changes the synthesis.
7. **Update `wiki/index.md`** — add newly created pages to the catalog.
8. **Write `ingest-complete` to `wiki/log.md`** — include the `Source:` path
   and list of all pages updated.

### Reading sources — order of preference

1. **`raw/extracted/<filename>.txt`** — use the Read tool directly. Fast and preferred.
2. **`raw/notes/<filename>.pdf`** — use the Read tool with `pages` parameter
   if no `.txt` exists.
3. **`raw/notes/<filename>.docx`** — use python-docx only as a last resort:

```python
from docx import Document
doc = Document('raw/notes/filename.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
print(text)
```

The `raw/extracted/` directory mirrors `raw/notes/` with the same base filenames
(`.docx` → `.txt`, `.pdf` → `.txt`).

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

- **Prefer updating existing concept pages** over creating new ones. Many
  sources cover the same concepts — build up one authoritative page per
  concept rather than duplicating across topics.
- **Summaries and checklists are gold.** If a source has a summary, checklist,
  or decision framework, extract it prominently into the topic page and
  the relevant concept pages.
- **Cross-source connections matter.** When a concept appears in multiple
  sources, note the cross-reference on the concept page.
