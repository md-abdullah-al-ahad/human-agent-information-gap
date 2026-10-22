# Comparative Literature & Methodology Analysis: Existing Web Agent Benchmarks vs. The Human–Agent Information Gap

## 1. Executive Summary

A common question in web agent research is: **Can existing benchmarking tools (such as BrowserGym, WebVoyager, or WebArena) be run on regional or live third-party websites instead of developing a dedicated information gap audit?**

Existing frameworks primarily evaluate navigation or task completion. The repository's item-level audit asks a different question, but its present labels and ground truth have the limitations described in [the consistency audit](repository-consistency-audit.md).

Existing benchmarks measure **macroscopic, end-to-end task completion** (treating the web interface and agent cognition as a black box). Our benchmark measures **microscopic, boundary-level information degradation** across the **4-stage pipeline**:
`[1. Surface Modality] -> [2. Tool-Exposed State] -> [3. Agent-Retrieved Context] -> [4. Agent-Reported Output]`.

This document is a working literature comparison. Its paper-level numerical claims have not been independently source-checked in this repository.

---

## 2. Taxonomy of Existing Literature

### A. Action-Driven & End-to-End Navigation Benchmarks
1. **WebArena (Zhou et al., CMU — July 2023, arXiv:2307.13854)**:
   - *Core Setup*: 812 tasks across 5 self-hosted, Dockerized web applications (GitLab, Shopping, Reddit, Map, CMS).
   - *Metric*: Binary task completion verified via direct SQL/database assertions (`assert order.status == 'completed'`).
   - *Limitation*: Relies on full control over backend databases. Cannot be pointed at live, third-party production websites where backend access is impossible.
2. **VisualWebArena (Koh et al., CMU / Google DeepMind — Jan 2024, arXiv:2401.13649)**:
   - *Core Setup*: 910 visually grounded tasks across 3 self-hosted websites (Classifieds, Shopping, Reddit). 25.2% of tasks feature input images.
   - *Key Results*: Human baseline 88.7%; text-only GPT-4 scored only **7.25%**; multimodal GPT-4V + Set-of-Marks reached **16.4%**. Tasks requiring OCR dropped to **13.4%**.
   - *Limitation*: Treats the visual agent as a monolith; if an agent fails, it cannot differentiate whether the failure was caused by DOM omission, visual encoder resolution, or planning derailment.
3. **WebVoyager (He et al., Tencent / HKUST — Jan 2024, arXiv:2401.13919)**:
   - *Core Setup*: End-to-end multimodal agent evaluated on 15 live websites using Selenium and Set-of-Marks.
   - *Failure Modes*: 44.4% navigation stuck (running out of steps in sub-scrollable panels), visual grounding errors on dense controls, and hallucination.
   - *Critical Flaw*: Evaluated via **GPT-4V as an automated judge**. Subsequent literature (*Emergence WebVoyager*, *Let's Think in Two Steps*) proved that LLM evaluators suffer from severe agreement bias, score partially completed tasks as successful, and fail to catch subtle factual errors.
4. **The BrowserGym Ecosystem (Chezelles et al., ServiceNow / Mila / CMU — Dec 2024, arXiv:2412.05467)**:
   - *Core Setup*: Unified gym-like wrapper around headless Chromium via Python **Playwright**.
   - *Contribution*: Standardized observation spaces (AxTree, DOM, Screenshot) and error propagation via `last_action_error` for Playwright DOM exceptions.
   - *Purpose*: Provides an execution runtime rather than an epistemological ground-truth auditor.

### B. Tool Learning & Interface Modernization
5. **WALT: Web Agents that Learn Tools (Prabhu et al., Salesforce Research — Oct 2025, arXiv:2510.01524)**:
   - *Core Finding*: Step-by-step UI clicking is fragile and breaks over long horizons. WALT synthesizes callable programmatic tools (action scripts) to replace 8+ UI clicks with 1 atomic operation, boosting VisualWebArena success from 16.4% to 52.9% (still far below 88.7% human capability).
6. **Build the web for agents, not agents for the web (Lù et al., McGill / Mila — Jun 2025, arXiv:2506.10953)**:
   - *Position*: Forcing agents to reverse-engineer human visual layouts via computer vision and DOM scraping strains web infrastructure and leads to brittle parsing. Proposes **Agentic Web Interfaces (AWIs)** offering structured schemas and progressive information streaming.
7. **Beyond Pixels: Exploring DOM Downsampling (Schiepanski & Piël — Aug 2025, arXiv:2508.04412)**:
   - *Empirical Discovery*: Raw HTML DOM snapshots exceed model context windows (128k tokens) in **42% of real-world websites**. Pruning saves tokens but destroys visual layout context and inline attributes.
8. **MolmoWeb (Gupta et al., Allen Institute for AI / UW — Apr 2026, arXiv:2604.08516)**:
   - *Key Discovery*: Non-visual AxTree teacher agents outperformed visual student agents by 5–10 points because visual models must perform implicit OCR across noisy screenshots and lack programmatic element identifiers.

---

## 3. Why Existing Benchmarking Tools Cannot Replace Our Audit on Live Sites

| Methodological Challenge | Existing Benchmark Tools (BrowserGym / WebVoyager) | Our Human–Agent Information Gap Benchmark |
|---|---|---|
| **Live Ground-Truth Verification** | Benchmark designs vary; live third-party state can be difficult to verify without backend access. | Researcher-annotated facts linked to captured surfaces. Eleven Stage-4 DOM/screenshot pairs have matching SHA-256 hashes, but hashes prove file integrity, not factual correctness or preregistration. |
| **Destructive / Financial Actions** | Cannot complete transactions on real e-commerce, banking, or ticketing portals without spending real currency or creating fake bookings. | Audits **informational and affordance integrity** across high-stakes domains (telecom, fintech, government, healthcare) without requiring fraudulent checkouts. |
| **Granularity of Failure Attribution** | **Binary End-State**: Output is `0` or `1`. Fails to explain *why* the model failed. | **Decomposed Boundary Analysis**: Traces the fact through 4 distinct physical boundaries to pinpoint whether the drop-off occurred in the tool, the agent retrieval, or the agent report. |
| **Cross-Modal Contradictions** | Treats image alt text or filenames as equivalent to visual content. | Probes **Pixel vs. Code Contradictions** (e.g., Chaldal Fresh vs. MGI asset filenames, Bikroy trapped raster watermarks). |
| **Economic & Cognitive Profiling** | Different suites emphasize different metrics. | Selected tool-ablation runs record longer retrieval loops without browser access; effects vary across sites and setups. |

---

## 4. Key Discoveries Unique to Our Benchmark

1. **The Trapped Raster Pixel Barrier**:
   - On Bikroy (BD-CL01), anti-fraud seller watermarks (`POSTED ON BIKROY <SELLER_NAME>`) have **0% DOM presence**.
   - In static conditions, LLMs completely dropped this information (`Not Found`), confirming that standard DOM extraction creates total informational blindness for non-visual tools.
2. **The Inverted Cost Paradox**:
   - Two recorded agent-run comparisons report higher API expense without Playwright; this is a selected observation, not a general effect:
     - OpenCode (Qwen 3.8 27B): $0.079 -> $0.159 (+100.1%).
     - Antigravity (Gemini 3.8 Flash): $0.068 -> $0.147 (+117.0%).
   - In some recorded runs, agents attempted many follow-up scripts and asset downloads.
3. **Dynamic Client Hydration & Skeleton Drop-Off**:
   - Modern Nuxt and React SSR shells deliver empty skeleton placeholders (`<div class="fw-skeleton-loader">`) for numerical metrics, misleading static tools into concluding data is absent.

---

## 5. Conclusion: Relationship Between Both Approaches

Existing benchmarking suites (like BrowserGym and WebVoyager) are **action drivers**—they test whether an agent can execute a policy graph to reach a target URL.

The repository's audit is an item-level diagnostic attempt across web modalities. Its scored claims require consistent adjudication before they can support strong cross-site accuracy conclusions.
