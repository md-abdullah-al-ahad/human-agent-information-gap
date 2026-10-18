# Stage 3 — Prospective Multi-Domain Information Gap Experiment Design (v0.2)

**Status:** Prospective research plan.  
**Project:** Human–Agent Information Gap across Website Modalities.  
**Objective:** Systematically measure where and why human-accessible website information fails to reach autonomous AI agents, evaluating information retention across four distinct website modalities:
1. Rendered HTML text and structured tables.
2. In-image text, diagrams, and banners.
3. Interactive UI elements requiring navigation/clicks.
4. Silent/absent fields and negative boundaries.

---

## 1. Core Experimental Framing

The goal is **not** to benchmark which LLM is smarter, nor to determine whether an agent can guess real-world product facts. 

The primary research objective is to calculate **Information Retention and Drop-off Rates across the 4-Stage Pipeline**:

$$\text{Information Gap Rate} = 1 - \frac{\text{Information Items Faithfully Conveyed in Agent Output}}{\text{Information Items Accessible to a Human on the Webpage}}$$

We measure where information drops off:
- **Gap 1 (Tool Barrier)**: Human-accessible information omitted by browser tools/scrapers (e.g., text embedded in images).
- **Gap 2 (Exploration Barrier)**: Tool-exposed information never inspected by the agent (e.g., unopened tabs, unclicked variants).
- **Gap 3 (Reporting & Inference Barrier)**: Retrieved information distorted in the final response, or absent information replaced with unsupported overconfidence.

---

## 2. Sampling Across Diverse Web Strata

To ensure findings are not idiosyncratic to e-commerce or a single marketplace, the prospective study expands across four distinct website domains:

1. **E-Commerce & Retail** (e.g., multi-variant consumer goods, technical accessories).
2. **Professional & Service Providers** (e.g., healthcare clinics, legal practices, consulting rate cards).
3. **Institutional & Public Portals** (e.g., university admissions, municipal service requirements).
4. **Technical Documentation & FAQs** (e.g., developer APIs, SaaS pricing tiers, refund/warranty policies).

**Sampling Rules**:
- Select public, reachable pages without requiring login or authentication.
- Freeze timestamped visual captures (full-page PDF/screenshots), raw DOM snapshots, and image assets at the exact selection time.

---

## 3. Experimental Conditions

To isolate the source of information loss, each selected page is evaluated under two controlled conditions:

### Track A: Natural Ecological Browsing
- The agent is provided with the live URL and a realistic user task (e.g., *"Find the eligibility criteria, deadline, and total fee for X"*).
- The agent freely operates Playwright MCP (navigating, clicking, snapshotting, and optionally downloading/viewing images).
- Measures real-world agent browsing behavior and exploration coverage (Gap 2).

### Track B: Sealed Evidence Bundles (Modality Ablation)
To determine whether information loss is driven by the browser tool or the agent's reasoning, models receive identical sealed evidence packets:
- **Condition B1 (Text & DOM Only)**: Markdown / accessibility snapshot of the page without image assets.
- **Condition B2 (Multimodal Text + Image Pixels)**: B1 text bundled with the actual raw image files and diagrams visible to a human.
- **Comparison**: Directly isolates the impact of the **In-Image Tool Barrier (Gap 1)** versus text processing.

---

## 4. Primary Metrics and Dependent Variables

For every audited page, human annotators establish the ground-truth **Information Item Inventory**. Each item is tagged with its source modality (`TEXT`, `IMAGE_TEXT`, `VISUAL_ONLY`, `DYNAMIC`, `ABSENT`).

We measure:
1. **Modality Retention Rate**: Proportion of human-accessible items in each modality that reach the agent's output.
2. **In-Image Drop-off Rate**: Percentage of critical statements located in images that are completely omitted by text-based browsing agents.
3. **Interactive Exploration Coverage**: Percentage of selectable variants/states inspected versus skipped.
4. **Affordance Overreach Rate**: Frequency with which active UI elements (buttons, links) are asserted as positive facts (e.g., inventory stock) in the absence of explicit data.
5. **Negative-Evidence Overreach Rate**: Frequency with which missing mentions in a menu/list are asserted as verified real-world physical incompatibilities.

---

## 5. Immediate Next Steps

1. Complete the independent human review of the P1–P3 Information Inventory using [`docs/stage-3-blind-human-review-worksheet.md`](stage-3-blind-human-review-worksheet.md).
2. Pre-select four candidate pages representing the four target strata (Retail, Services, Public, Documentation).
3. Freeze page captures and pre-construct the Information Inventories before initiating Track A and Track B agent runs.
