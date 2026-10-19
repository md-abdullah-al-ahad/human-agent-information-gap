# Related Literature Index: Web Agents, Multimodal Grounding & The Information Gap

This directory contains the primary research literature directly relevant to the **Human–Agent Information Gap across Web Modalities**.

---

## 1. Catalog of Acquired Literature

| Directory | Paper Title | Authors & Affiliation | Year / Date | ArXiv ID | Core Modality & Setup |
|---|---|---|---|---|---|
| [`visualwebarena/`](./visualwebarena/) | **VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks** | Koh et al. (CMU, Google DeepMind) | Jan 2024 | `2401.13649` | 910 tasks across 3 self-hosted platforms (Classifieds, Shopping, Reddit). Evaluates Text vs. VLM vs. Set-of-Marks. |
| [`build-web-for-agents/`](./build-web-for-agents/) | **Build the web for agents, not agents for the web** | Lù et al. (McGill University, Mila) | Jun 2025 | `2506.10953` | Position paper proposing Agentic Web Interfaces (AWIs) to replace fragile UI scraping. |
| [`webvoyager/`](./webvoyager/) | **WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models** | He et al. (Tencent, HKUST) | Jan 2024 | `2401.13919` | End-to-end visual agent evaluated across 15 live real-world websites using Selenium and Set-of-Marks. |
| [`walt-web-agents-learn-tools/`](./walt-web-agents-learn-tools/) | **WALT: Web Agents that Learn Tools** | Prabhu et al. (Salesforce Research) | Oct 2025 | `2510.01524` | Synthesizes callable programmatic tools from web exploration traces to eliminate fragile UI step sequences. |
| [`beyond-pixels-dom-downsampling/`](./beyond-pixels-dom-downsampling/) | **Beyond Pixels: Exploring DOM Downsampling for LLM-Based Web Agents** | Schiepanski & Piël | Aug 2025 | `2508.04412` | Evaluates DOM token explosion and introduces D2Snap for tree downsampling. |
| [`browsergym-playwright/`](./browsergym-playwright/) | **The BrowserGym Ecosystem for Web Agent Research** | Chezelles et al. (ServiceNow, Mila, CMU) | Dec 2024 | `2412.05467` | Core gym-like framework wrapping Chromium via Playwright for standardized multimodal web agent evaluation. |
| [`browseragent-playwright/`](./browseragent-playwright/) | **BrowserAgent: Building Web Agents with Human-Inspired Web Browsing Actions** | Yu et al. | Oct 2025 | `2510.10666` | Directly operates on raw web pages via Playwright actions; parallelizes Playwright with Ray. |
| [`internal-apis-vs-playwright/`](./internal-apis-vs-playwright/) | **Internal APIs Are All You Need: Shadow APIs vs. Browser-First Agent Architectures** | Tham, Mac Gregor Garcia, Hahn | Apr 2026 | `2604.00694` | Direct live-web empirical benchmark comparing Playwright browser automation against direct internal API calls across 94 domains. |
| [`playwright-agent-detection/`](./playwright-agent-detection/) | **What Does It Take to Detect an AI Agent? Minimal Feature Sets under Browser Automation** | Choudhary et al. | Jul 2026 | `2607.26935` | Analyzes Playwright's behavioral DOM signatures (pointer-move absence, click teleportation) and anti-bot detection. |
| [`molmoweb/`](./molmoweb/) | **MolmoWeb: Open Visual Web Agent and Open Data for the Open Web** | Gupta et al. (Allen Institute for AI, UW) | Apr 2026 | `2604.08516` | State-of-the-art open 4B/8B multimodal web agent trained on 2,700 trajectories and atomic skill mixtures. |
| [`webarena/`](./webarena/) | **WebArena: A Realistic Web Environment for Building Autonomous Agents** | Zhou et al. (CMU) | Jul 2023 | `2307.13854` | The foundational realistic web benchmark across 5 self-hosted web applications. |

---

## 2. Cross-Paper Experimental Comparison

### A. How Prior Work Ran Experiments
1. **VisualWebArena (2024)**:
   - **Environment**: Dockerized, self-hosted web applications (Shopping, Classifieds, Reddit) to guarantee determinism.
   - **Observation Space**: Compared raw HTML, Accessibility Trees (AxTree), Full Screenshots, and Set-of-Marks (SoM) bounding boxes.
   - **Evaluation Metric**: Binary task success rate (reaching expected database or end-state).
   - **Key Finding**: Humans succeed at **88.7%**. Text-only GPT-4 scores only **7.25%**. Multimodal GPT-4V + SoM reaches **16.4%**. Tasks requiring OCR dropped performance to **13.4%**.

2. **WebVoyager (2024)**:
   - **Environment**: Live, open-web navigation across 15 real-world websites (Amazon, Apple, Booking, Google Flights, etc.) via Selenium.
   - **Observation Space**: Screenshots with Set-of-Marks element numbering.
   - **Error Taxonomy**:
     - **44.4% Navigation Stuck**: Agents get trapped in loops, cannot locate sub-scrollable panels, or get derailed by noisy search results.
     - **Visual Grounding Failures**: Misinterpreting visual numerals on calendar widgets as Set-of-Marks labels; element proximity confusion.
     - **Hallucination**: Prematurely answering without sorting or verifying criteria.

3. **Build the Web for Agents, Not Agents for the Web (2025)**:
   - **Core Thesis**: Forcing agents to reverse-engineer human visual interfaces via computer vision and DOM scraping is fundamentally flawed.
   - **Proposed Paradigm**: Websites should serve dual interfaces—a visual UI for humans, and an **Agentic Web Interface (AWI)** providing structured state schemas, atomic actions, access controls, and progressive information streaming.

4. **WALT: Salesforce Research (2025)**:
   - **Setup**: Evaluated on WebArena and VisualWebArena. Replaces 8–15 fragile UI clicks with synthesized deterministic action scripts.
   - **Results**: Boosted VisualWebArena success to **52.9%** (the state-of-the-art in late 2025), but highlights that the gap to human performance (88.7%) remains substantial (~36% failure rate).

5. **Beyond Pixels (2025)**:
   - **Empirical DOM Analysis**: Proves that raw web DOMs exceed LLM context windows (128,000 tokens) in **42% of real-world cases**.
   - **The Tradeoff**: Pruning nodes saves tokens but destroys visual layout context, dynamic states, and inline visual metadata.

6. **MolmoWeb: Allen Institute for AI (2026)**:
   - **Setup**: Open multimodal agent (4B and 8B) trained on synthetic and human browsing trajectories.
   - **Crucial Finding**: Non-visual AxTree teacher agents outperformed visual student agents by 5–10 points on WebVoyager and DeepShop. Visual models struggled with implicit OCR over screenshots and precise coordinate pointing.

---

## 3. How Our Research Specifically Differs and Advances Beyond Prior Work

| Evaluation Dimension | Prior Literature (WebArena, VisualWebArena, WebVoyager, MolmoWeb) | Our Research (Human–Agent Information Gap Benchmark) |
|---|---|---|
| **Core Research Question** | *"Can the agent accomplish a multi-step task on the web?"* (End-to-End Success Rate) | *"Where, why, and across which modalities does web information become invisible or corrupted for agents?"* (The 4-Stage Pipeline) |
| **Granularity of Measurement** | **Macroscopic End-State**: Success = 1 if the order was placed or final URL reached; 0 otherwise. | **Microscopic Boundary Tracing**: Traces every factual unit across `[1. Surface] -> [2. Tool-Exposed] -> [3. Agent-Retrieved] -> [4. Agent-Reported]`. |
| **Visual Stress Modalities** | General e-commerce product photos and standard UI buttons. | **Trapped Pixel Information**: In-photo seller watermarks, trapped banner instructions, dynamic overlays, skeleton loaders, and misleading asset filenames. |
| **Ablation Architecture** | Tests Text vs VLM within a single agent framework. | **Strict 2x2 Factorial Tool Ablation**: Head-to-head comparison of With Playwright vs. Without Playwright across OpenCode (Qwen 3.8 27B) and Antigravity (Gemini 3.8 Flash). |
| **Cost & Latency Discovery** | Treats cost as secondary or monotonic with step count. | **The Inverted Cost Paradox**: Proves that ablating browser tools *doubles* token consumption and cost due to runaway compensatory scripting loops. |
