# Site BD-01: Shohoz Bus Tickets — Controlled Playwright vs. Static Tool Ablation Audit

**Target URL:** `https://www.shohoz.com/bus-tickets/`  
**Platform Architecture:** Angular Single Page Application (SPA)  
**Evaluation Date:** 2026-10-19  
**Experimental Design:** Controlled 2x2 Factorial Tool Ablation (With Playwright vs. Without Playwright across OpenCode/Qwen and Antigravity/Gemini).  
**Contamination Check:** Both static sessions were executed in brand-new chats with zero access to past logs, results, or file paths.

---

## 1. Provenance and Runtime Resource Metadata

| Evaluation Condition | Setup & Model | Session ID | Retrieval Tooling | Input Tokens (Uncached) | Cache Read Tokens | Output Tokens | Total Processed Tokens | Billed / Equiv Cost | Wall-Clock Latency |
|---|---|---|---|---|---|---|---|---|---|
| **Condition 1 (With Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eae9ad800ffeZ509pRDKhKu4k5` | `playwright_browser_navigate`, `snapshot` | **21,078** | **67,760** | **691** (866 reas) | **89,704** | **$0.011872** (OpenRouter) | **24.8 s** |
| **Condition 1 (With Playwright)** | Antigravity / Gemini 3.8 Flash | `c85e3f7b-61db-4eb1-9e66-19f7ee39147c` | `call_mcp_tool` Playwright Chromium | **121,416** | **330,624** | **6,625** | **458,665** | **$0.017293** (Gemini Rate Card) | **98.0 s** |
| **Condition 2 (Without Playwright)** | OpenCode / Qwen 3.8 27B | `ses_eae8f8c39ffevoh8dNyDFfOID6` | `webfetch` (pure HTTP fetch) | **15,600** | **0** | **404** (244 reas) | **16,248** | **$0.005797** (OpenRouter) | **14.4 s** |
| **Condition 2 (Without Playwright)** | Antigravity / Gemini 3.8 Flash | `b5dfe6ef-3ce6-4e67-8744-927aa34ae524` | `read_url_content` + 18 Python parsers | **125,230** | **1,014,244** | **9,591** | **1,149,065** | **$0.031287** (Gemini Rate Card) | **118.0 s** |

---

## 2. Evaluation Against Researcher-Annotated Reference (22 Items)

| Item ID | Target Information Fact | Modality Surface | Human Ground Truth | Qwen (With Playwright) | Gemini (With Playwright) | Qwen (Without Playwright) | Gemini (Without Playwright) | Empirical Tool Ablation Finding |
|---|---|---|---|---|---|---|---|---|
| **BD1-01** | Platform Identity | `TEXT` | Shohoz / Shohoj Limited | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-02** | Main Service Heading | `TEXT` | Book & Buy Bus Tickets Online | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-03** | Search Input: Origin | `DYNAMIC` | `From` station input | **Yes** | **Yes** | **Yes** | **Yes** | Present in static template |
| **BD1-04** | Search Input: Destination | `DYNAMIC` | `To` station input | **Yes** | **Yes** | **Yes** | **Yes** | Present in static template |
| **BD1-05** | Search Input: Journey Date | `DYNAMIC` | `Journey Date` ("Pick a date") | **Yes** | **Yes** | **Yes** | **Yes** | Present in static template |
| **BD1-06** | Trip Type Selector | `DYNAMIC` | `One Way` vs `Round Way` | **Yes** | **Yes** | **Yes** | **Yes** | Present in static template |
| **BD1-07** | Return Trip Add Button | `DYNAMIC` | `+ ADD RETURN TRIP` | **Yes** | **Yes** | **Yes** | **Yes** | Present in static template |
| **BD1-08** | Trending Destinations | `TEXT` | Chittagong, Dhaka, Rajshahi, etc. | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-09** | Featured Operators | `TEXT` | Nabil, SR, Shohagh, Royal Coach, etc. | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-10** | Operator Count Metric | `TEXT` | 100+ operators nationwide | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-11** | Scale Metrics | `TEXT` | 250M+ tickets, 10M+ users | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-12** | Support Helpline | `TEXT` | `16374` | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-13** | Helpline Operating Hours | `TEXT` | `7 AM - 11 PM` | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-14** | Support Email | `TEXT` | `info@shohoz.com` | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-15** | Purchase Channels | `TEXT` | Web, Android/iOS App, 16374 | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-16** | Purchase Time Window | `TEXT` | 24/7 web; helpline 7 AM - 11 PM | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-17** | Cancellation Time Limit | `TEXT` | 12/24 hours before departure | **Yes** | **Yes** | **Yes** | **Yes** | Static parity |
| **BD1-18** | **Negative Blackout Window** | `EXPLICIT_NEGATIVE` | **Excluding 11 PM to 7 AM** | **Yes** (Verbatim) | **Yes** (Verbatim) | **Yes** (Verbatim) | **Yes** (Verbatim) | **RQ4: Zero overreach in all setups** |
| **BD1-19** | **Mandatory Migration Rule** | `TEXT` | **Must call from booking phone number** | **Yes** (Verbatim) | **Yes** (Verbatim) | **Yes** (Verbatim) | **Yes** (Verbatim) | Critical prerequisite preserved |
| **BD1-20** | **Refund: bKash/Nagad** | `TEXT` | **Maximum 5–7 working days** | **Yes** (Exact) | **Yes** (Exact) | **Yes** (Exact) | **Yes** (Exact) | Static parity |
| **BD1-21** | **Refund: Cards/Banking** | `TEXT` | **Maximum 7–10 working days** | **Yes** (Exact) | **Yes** (Exact) | **Yes** (Exact) | **Yes** (Exact) | Static parity |
| **BD1-22** | **Unified Login Scope** | `DYNAMIC` | Single account for **`Bus, Air, and Park`** | **Yes** (`Bus, Air, and Park`) | **Yes** (`Bus, Air, and Park`) | **FAILED** (Heuristic guess: 6 services) | **FAILED** (Heuristic guess: 6 services) | **Gap 1 Confirmed in Both Static Runs** |

---

## 3. Key Empirical Findings from the Tool Ablation

### Finding 1: The Deterministic Dynamic Hydration Barrier (Item BD1-22)
- **Question Asked**: *"What services are covered under the single Shohoz account?"*
- **Ground Truth**: A green notification banner rendered above trending destinations reads:
  > *"Welcome to a Smarter Shohoz Login! If you're an existing user, just reset your password once to continue. Now access **Bus, Air, and Park** with a single Shohoz account. Easy and secure!"*
- **Condition 1 (With Playwright — Qwen & Gemini)**:
  - Both models executed Chromium, waited for Angular DOM hydration, and extracted the exact three services: **`Bus, Air, and Park`** (100% precision).
- **Condition 2 (Without Playwright — Qwen & Gemini)**:
  - In the unhydrated static HTML scrape, the dynamic banner was completely missing.
  - **Both models exhibited identical failure behavior**:
    - Qwen reported: *"Services under the single Shohoz account: Bus, Air, Train, Launch, Event, and Park (Beta) tickets."*
    - Gemini reported: *"The phrase 'single Shohoz account' does not appear verbatim... unified navigation features: Bus, Air, Train, Launch, Event, Park."*
  - **Scientific Conclusion**: *Without Playwright, client-side dynamic announcements are completely lost to AI agents. Both models fall back to heuristic guessing from static navigation elements.*

### Finding 2: Robust Preservation of Explicit Negative Constraints (RQ4 on BD1-18)
- Shohoz specifies an explicit negative blackout window:
  > *"12/24 hours excluding 11 PM to 7 AM"*
- Across all 4 independent runs (Playwright and Static, Qwen and Gemini), **all models preserved the negative boundary with 100% precision**. This further proves that explicit negative syntax eliminates agent overreach regardless of retrieval tooling.

### Finding 3: The Economic Cost-Benefit Frontier and Architectural Divergence
- **Single-Pass Tool Agent (OpenCode / Qwen)**:
  - Playwright cost **$0.011872** (21,078 input tokens, 24.8 s) versus **$0.005797** (15,600 input tokens, 14.4 s) for static fetch (**2.05x cost multiplier, 1.35x token bloat**).
  - Here, disabling Playwright cut cost by 51% because the model made a single lightweight `webfetch` call.
- **Autonomous Multi-Step Code Execution Agent (Antigravity / Gemini)**:
  - Playwright required **21 LLM steps** (121,416 uncached input tokens, 330,624 cached tokens, 458,665 total tokens, **$0.017293** equivalent cost, 98.0 s).
  - Without Playwright, the agent was forced to execute **18 iterative Python and Bash parsing scripts** (`sed`, `grep`, BeautifulSoup, `html.parser`), resulting in **23 LLM steps** (125,230 uncached input tokens, 1,014,244 cached tokens, 1,149,065 total tokens, **$0.031287** equivalent cost, 118.0 s).
  - **Empirical Discovery**: For an autonomous code-executing agent, **depriving it of Playwright actually increased total processed tokens by 2.5x and increased cost by 81%**, because the model burned massive context iterative parsing unrendered HTML.
- **Information Trade-off**: Static fetch retrieved 21 of 22 items (95.5%). However, capturing the dynamic client-side Angular banner strictly required headless browser execution.
