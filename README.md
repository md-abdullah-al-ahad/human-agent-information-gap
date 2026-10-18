# Human–Agent Information Gap

An empirical research project investigating the gap between information human users can perceive and verify on modern websites, and the information autonomous AI browsing agents reliably retrieve, interpret, and report.

---

## 1. Research Objectives

When humans browse the web, they integrate rendered typography, contextual styling, embedded imagery, diagrams, and dynamic UI affordances. Autonomous AI browsing agents, however, interact with websites through intermediate layers (accessibility trees, DOM snapshots, API scrapers, or browser-automation protocols).

This research investigates:
1. **The Information Accessibility Pipeline**: Where does human-accessible information drop off across the boundary between website, browser tools, agent exploration, and final output?
2. **Modality Barriers**: How does information retention vary when critical facts are stored in plain HTML text versus raster images, dynamic JavaScript dropdowns, or pure visual affordances?
3. **Inference Overreach & Uncertainty**: When an information item is missing or silent on a website (e.g., warehouse stock levels or unlisted device compatibility), under what conditions do agents appropriately abstain versus making unsupported, overconfident positive or negative assertions?

---

## 2. The 4-Stage Information Pipeline Model

```
[Stage 1: Website & Human Surface] 
  Rendered text, structured attributes, in-image graphics, interactive states
       │
       ▼  GAP 1: Tool Exposure Barrier (What Playwright/DOM/Scraper exposes)
[Stage 2: Tool-Exposed Information]
  Accessibility tree, DOM snapshot, evaluate scripts, downloaded media
       │
       ▼  GAP 2: Agent Exploration & Retrieval Barrier (What the agent actually inspects)
[Stage 3: Agent-Retrieved Information]
  Content retrieved into the agent context and tool histories
       │
       ▼  GAP 3: Output Reporting & Inference Barrier (What the agent conveys vs. invents)
[Stage 4: Final Reported Output]
  Information faithfully communicated, omitted, or converted into unsupported claims
```

---

## 3. Repository Structure

```
├── docs/
│   ├── audit-protocol.md                         # Stage 1 audit protocol (v0.2) and question families (Q1-Q9)
│   ├── pilot-01-findings.md                      # Provisional findings from initial 3-page Daraz pilot
│   ├── stage-3-reference-adjudication.md         # Grounded reference of human-accessible surfaces (P1-P3)
│   ├── stage-3-blind-human-review-worksheet.md   # Blank worksheet for independent human surface audit
│   └── stage-3-next-experiment-design-v0.1.md    # Multi-domain follow-up experiment design (Tracks A & B)
├── data/
│   └── pilot-01/
│       ├── selection.json                        # Query ranks, URLs, and sampling rules for P1-P3
│       ├── observations.json                     # Structured pilot observations for Q1-Q9
│       ├── addendum-01.json                      # Independent Chrome headless verification of alternate SKUs
│       ├── screenshots/                          # Timestamped initial and alternate viewport PNGs
│       ├── raw/                                  # Firecrawl scrapes, search logs, and browser interact files
│       └── human-capture-P*-ai-review.json       # AI-assisted audits of human print-to-PDFs
└── results/
    ├── information-gap-results-template.csv      # Standard tabular schema for information-item drop-off
    ├── pilot-results-template.csv                # Legacy per-question evaluation template
    └── experiment-01/
        ├── information-inventory-matrix-p1-p3.md # Itemized 41-item empirical inventory across P1-P3
        ├── cross-case-synthesis-p1-p3.md         # Cross-case synthesis of agent browsing behaviors
        ├── P1/                                   # Trace audit and raw outputs for P1 (ESR Screen Protector)
        ├── P2/                                   # Paired trace audit and raw outputs for P2 (2PCS Screen Protector)
        └── P3/                                   # Paired trace audit and raw outputs for P3 (3+Y-fold Folio Case)
```

---

## 4. Empirical Status (Pilot 01 / Experiment 01)

- **Dataset**: Three diverse e-commerce listings audited on Daraz Bangladesh:
  - **P1**: ESR Magnetic Paper-Feel Removable Screen Protector.
  - **P2**: 2PCS Glass Screen Protector (with ambiguous "Case/Cover" in title).
  - **P3**: 3+Y-fold Clear iPad Folio Case.
- **Instruments**: Two paired agent setups equipped with Playwright MCP:
  - `OpenCode` running `qwen/qwen3.8-27b` (Medium) via OpenRouter.
  - `Antigravity CLI` running `Gemini 3.8 Flash` (Medium).
- **Core Findings to Date**:
  - **Interactive State Success**: Both agents successfully manipulated dynamic UI selectors to extract correct alternate SKU prices and URLs across all three pages.
  - **The In-Image Tool Barrier (Gap 1)**: When critical specifications or model restrictions were embedded inside images (e.g., P1 restrictive compatibility notice), DOM snapshots suffered a 100% omission rate. Information was only accessible when agents took extra shell steps to download and view image pixels.
  - **Affordance-to-Stock Overreach (Gap 3)**: In 6 out of 6 runs, both agents asserted items were "in stock" despite empty stock fields, relying solely on active purchase buttons.
  - **Negative-Evidence Overreach (Gap 3)**: Both agents repeatedly converted the absence of a device option in a selector menu into a definitive claim of physical device incompatibility.

---

## 5. Next Steps

1. Complete independent human verification using [`docs/stage-3-blind-human-review-worksheet.md`](docs/stage-3-blind-human-review-worksheet.md).
2. Execute the multi-domain prospective expansion ([`docs/stage-3-next-experiment-design-v0.1.md`](docs/stage-3-next-experiment-design-v0.1.md)) across Retail, Professional Services, Public Portals, and Technical Documentation.
3. Compare free ecological browsing (Track A) against controlled sealed packets with and without image pixels (Track B) to formally quantify Gap 1 and Gap 2 across the web.
