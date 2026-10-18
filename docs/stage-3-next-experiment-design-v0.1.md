# Stage 3 — Prospective follow-up experiment design v0.1

**Status:** DRAFT, prospective plan; not preregistered, not yet executed.  
**Project:** Human–Agent Information Gap (all website information domains, not solely shopping).
**Prepared:** 2026-10-18.

## Research question

When information is human-accessible on a website but distributed across text, images, dynamic controls, or missing/ambiguous mentions, what evidence can an AI browsing agent retrieve and what conclusions does it make? In particular, under what conditions does it make unsupported **positive** or **negative** claims rather than appropriately constrain the answer?

This work explicitly separates:

- **Human-visible source facts**: what the page states/displays in a defined frozen state.
- **Agent-accessed evidence**: what its recorded tools returned in its own session.
- **Agent assertion**: what the final answer claims and with what wording.
- **Product/service reality**: external truth, often impossible to verify from the page alone.

## Why the first six runs do not answer this yet

P1–P3 used only three Daraz pages with preexisting AI-assisted references. Different models had different tooling patterns and page times. No human-blinded adjudication or held-out sampling. Therefore the observed repeated inventory/incompatibility inferences are hypotheses, **not prevalence estimates**.

## Experimental tracks

### Track A: Ecological, agent-controlled website browsing

- Use fresh, preselected publicly reachable pages from **at least four types of sites**, e.g. retail product; services or professional providers; institutional information; documentation or policy/FAQ. Domains should be preselected with a reproducible rule and include **non-shopping pages**.
- Human reviewers freeze a page at time of selection (screenshots/PDF, DOM, important images, accessible locale, URL, timestamp, viewport, selected state). Capture browser/server errors, login state and failed eligibility candidates.
- Prompt each agent with a **realistic question in the relevant domain**. Tell it to use Playwright MCP and supply the URL. Do **not** disclose performance testing, missing-data taxonomy, desired hedging behavior, or correct answer.
- Preserve raw tool calls/responses and final output unchanged; no special requirement to exhaustively inspect every image or click every control. That choice is part of measured agent behavior.
- Compare retrieval coverage and conclusions with independently annotated human-visible evidence; record any drift between the frozen capture and agent view.

### Track B: Controlled common-evidence interpretation

- For the *same question on the same selected new page*, give each model an **identical sealed evidence packet** representing a defined capture at one time. Avoid injecting interpretation/answer labels.
- Subconditions, if feasible:
  - **B1**: textual DOM/snapshot and relevant attribute/value output only;
  - **B2**: exactly B1 plus the corresponding **original pixels** of page/gallery/promotional images;
  - optionally **B3**: complete renderer screenshot + DOM; document any confounding differences.
- The agent does not browse in B1/B2. Use a short, neutral “I am trying to find out X; use this saved page material” task statement, not a rubric about uncertainty.
- Distinguish effect of **adding image evidence** (B1 vs B2) from effect of **agent-chosen browsing** (A vs B2). Because packet presentation also changes relevance and context length, do **not** claim this perfectly isolates a single causal variable.
- Provide all models the same questions, evidence version, media files, and maximum response budget. Match context and modality support as well as possible; report any differences.

### Track C (later): Deliberately controlled negative-evidence cases

After Track A/B feasibility, develop small website fixtures or pair carefully matched real pages to separate:
1. explicit negative statement (“not supported”);
2. explicit exhaustive list (“supported models are only A/B”);
3. positive but nonexhaustive examples (“e.g., A/B”);
4. no mention;
5. conflicting title, table and image.

For artificial fixtures, vary exactly the relevant statement while holding design and rest of content fixed. Test claims and abstention without revealing to the agent that uncertainty handling is the independent variable. Label synthetic stimuli as such; never mix with real-world estimates.

## Feasibility sample and budget

**Suggested feasibility only**: four *new* pages (one per domain), one core question per page with a state-changing follow-up only where natural, two agent setups, and three conditions (A, B1, B2): **4 × 2 × 3 = 24 first-pass outputs**. Repeats can be added only after estimating run-to-run variance and cost. For the Qwen setup this is 12 runs; using the observed P1–P3 per-run OpenCode billed costs ($0.0286 / $0.1182 / $0.0781) as *loose illustrative anchors*, its portion might consume roughly $0.3–$1.4 before retries; **not a guarantee**. Gemini entitlement or compute cost is unverified. Apply hard credit/rate limits before running.

**Expansion if feasible**: 12 new pages across four strata (3 each), with the same two setups and conditions, for 72 first-pass outputs. This number is **not powered for inferential estimates**. Do not treat multiple questions on the same page as statistically independent.

## Sampling and exclusion rules (freeze before browsing)

- One stable canonical page per eligible selection; record discovery method, ordering/rank, attempt/rejection logs, language, region, public/logged-out reachability, and page snapshot timestamp.
- Avoid pages requiring account access, payment, bypassing access controls or personal data.
- Predeclare what counts as human-visible: after normal scrolling and opening ordinary public tabs/accordion/details, without bypassing security or obtaining external proprietary data.
- Prefer changing only one question-level difficulty at a time; on highly dynamic pages require consistent selected state and capture enough to detect drift.
- Existing P1–P3 are for **hypothesis generation only**; do not use them as the primary prospective evaluation set.

## Annotation unit and metrics

Primary unit: **(page, selected state, question, agent, condition, run)**. Cluster analysis at the page/site level; do not count multiple correlated subquestions as independent page samples.

For every response sentence/claim, human annotators should tag:
- `claim_polarity`: positive / negative / uncertain / neutral;
- `answer_status`: answered / abstained / conditional / contradictory;
- `source_status`: explicitly supported by reference / directly visible but inferred / contradicted / conflict / not observed / external unverified;
- `agent_exposure`: retrieved evidence found in logged tool output / not found / trace missing / image-view pixels unavailable;
- `scope`: site-wide / page-level / variant-level / time-limited / external reality;
- `support_strength`: properly qualified / overstated / underclaimed / not judgeable;
- `true_fact_status`: verified / unknown (typically unknown for stock, physical compatibility and charging).

Candidate rates (only when denominators/labels are valid):
- **Evidence access**: relevant human-visible items that appeared in recorded agent-readable content / relevant captured items with accessible modality. Report by modality and state.
- **Unsupported negative assertion rate**: unsupported negative claims / all substantive negative claims, with itemized scope.
- **Unsupported affirmative assertion rate**: unsupported affirmative claims / all substantive affirmative claims.
- **Appropriate abstention**: justified uncertainty when evidence is silent/contradictory; score separately from answer correctness.
- **Variant-state accuracy**: correctly attributed displayed price/features to requested state / audited state-change tasks.
- **Task completion and tool use**: clicks, snapshots, screenshots, errors, image inspection, duration, cost where provider reports it.

These are source-support measures, not direct tests of whether the page's seller statements are truthful. Predeclare primary and secondary endpoints before any confirmatory study.

## Blind adjudication and model isolation

- Human source annotators get original snapshots and questions only, **not model outputs**, proposed failure labels, or prior AI annotations.
- Have two independent reviewers for difficult cases when feasible; disagreements resolved in a dated adjudication log retaining both original labels.
- Agents get no critique, no previous runs, no research hypotheses, and no previous browsing findings.
- Use fresh sessions; record explicit model/provider/version, agent wrapper, reasoning setting, browser/Playwright version, enabled other tools, time, locale, resolution and login status.
- If an agent cannot preserve original image pixels or tool outputs, report evidence-access status as unknown rather than inventing an observation.
- If agents use extra tools (e.g., shell downloads/image viewer) as they did in P2/P3, record that; Track A compares full systems rather than isolated model weights.

## Practical order of work

1. Complete blinded P1–P3 human review using `docs/stage-3-blind-human-review-worksheet.md`; reconcile P3 Pencil and P2 package questions while leaving unsolved ones `UNRESOLVED`.
2. Prospectively select **four new nonidentical pages** from distinct site types, record eligibility/sampling before model exposure, freeze snapshots.
3. Choose one narrowly scoped, human-natural question per selected page.
4. Generate B1/B2 packets from exactly those snapshots and verify byte/checksum equality for each model.
5. Run A/B1/B2 in separate fresh sessions; preserve original outputs/traces; refrain from commenting to the agents on any finding.
6. Blind-score source evidence independently of agent answers, then audit exposure and classify agent claims.
7. Decide after feasibility whether to expand, repeat, add model settings, or discard hypotheses without promise of a publishable effect.

## Integrity warning

The strongest current *observation* is overconfident claims relative to visible website evidence, not proven product mistakes or a prevalence estimate. A website's missing statement is not automatically evidence that the underlying fact is false. No proposed condition should teach evaluated agents the desired answer style.
