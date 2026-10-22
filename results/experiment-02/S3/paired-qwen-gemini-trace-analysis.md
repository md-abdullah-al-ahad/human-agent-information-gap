# S3: Gov.uk Standard Visitor Visa — Paired Agent & Tool Trace Audit (Track A)

**Status:** Completed empirical evaluation for S3 (Track A Live Browsing).  
**Evaluation Date:** 2026-10-19.  
**Evaluated Agents:**
1. **OpenCode / Qwen 3.8 27B Medium** (OpenRouter)
2. **Antigravity CLI / Gemini 3.8 Flash Medium** (Google)
**Tooling Environment:** Playwright MCP (OpenCode) / Web fetch & HTML parser (Antigravity).

---

## 1. Provenance and Runtime Metadata

| Measure | OpenCode / Qwen 3.8 27B | Antigravity / Gemini 3.8 Flash |
|---|---|---|
| **Session ID** | `ses_eaf4d32eaffeUHor17f7qbCuVt` | `8d899430-88cf-4ad3-a6ef-7235562f386b` |
| **Execution Timestamp** | 2026-10-19 02:27:37 Asia/Dhaka | 2026-10-19 02:27:39 Asia/Dhaka |
| **Retrieval Tool Strategy** | Playwright MCP: `browser_navigate` (1), `browser_snapshot` (1) | `read_url_content` (1), Python HTML DOM parser (2) |
| **Additional Tools Invoked** | None (pure single-pass accessibility snapshot) | Worklog update |
| **Session Cost** | **$0.006316** (OpenRouter billed cost) | Billed per Google subscription (not exposed in export) |
| **Token Usage** | Input: 16,150; Output: 587; Reasoning: 228 | Input: ~28,000; Output: ~2,400 |
| **Raw Answer File** | [`opencode-qwen-user-exported-answer.md`](opencode-qwen-user-exported-answer.md) | [`antigravity-gemini-user-exported-answer.md`](antigravity-gemini-user-exported-answer.md) |
| **Full Session JSON** | [`opencode-qwen-session.json`](opencode-qwen-session.json) | [`antigravity-gemini-session.json`](antigravity-gemini-session.json) |

---

## 2. Evaluation Against Researcher-Annotated Reference (16 Items)

| Item ID | Target Information Item | Modality Surface | Human Ground Truth | Qwen Retrieved & Reported | Gemini Retrieved & Reported | Information Gap Classification |
|---|---|---|---|---|---|---|
| **S3-01** | Visa Category | `TEXT` | `Standard Visitor` | **Yes** (`Standard Visitor`) | **Yes** (`Standard Visitor`) | None (Retained) |
| **S3-02** | Standard Maximum Stay | `TEXT` | Up to 6 months | **Yes** (`up to 6 months`) | **Yes** (`up to 6 months`) | None (Retained) |
| **S3-03** | Visa Application Fee | `TEXT` | `£135` (Current official fee on page) | **Yes** (`£135`) | **Yes** (`£135`) | None (Retained; live ground truth verified) |
| **S3-04** | Permitted: Tourism / Holiday | `TEXT` | Tourism, holiday or vacation | **Yes** (Exact scope quoted) | **Yes** (Exact scope quoted) | None (Retained) |
| **S3-05** | Permitted: Family & Friends | `TEXT` | See your family or friends | **Yes** (Exact scope quoted) | **Yes** (Exact scope quoted) | None (Retained) |
| **S3-06** | Permitted: Volunteering | `TEXT` | Volunteer up to 30 days with registered charity | **Yes** (Reported with 30-day limit) | **Yes** (Reported with 30-day limit) | None (Retained) |
| **S3-07** | Permitted: Transit | `TEXT` | In transit to another country | **Yes** (Exact scope quoted) | **Yes** (Exact scope quoted) | None (Retained) |
| **S3-08** | Permitted: Business Meetings | `TEXT` | Attending a meeting or interview | **Yes** (Exact scope quoted) | **Yes** (Exact scope quoted) | None (Retained) |
| **S3-09** | Permitted: Short Study / Placement | `TEXT` | Study, placement or exam (up to 6 months) | **Yes** (Exact scope quoted) | **Yes** (Exact scope quoted) | None (Retained) |
| **S3-10** | **Prohibition 1: UK Employment** | `EXPLICIT_NEGATIVE` | No paid/unpaid work for UK company or self-employed | **Yes** (Quoted verbatim) | **Yes** (Quoted verbatim) | None (**Zero negative overreach**) |
| **S3-11** | **Prohibition 2: Public Funds** | `EXPLICIT_NEGATIVE` | Cannot claim public funds (benefits) | **Yes** (Quoted verbatim) | **Yes** (Quoted verbatim) | None (**Zero negative overreach**) |
| **S3-12** | **Prohibition 3: Frequent Long Stays** | `EXPLICIT_NEGATIVE` | Cannot live in UK via frequent/successive visits | **Yes** (Quoted verbatim) | **Yes** (Quoted verbatim) | None (**Zero negative overreach**) |
| **S3-13** | **Prohibition 4: Marriage / Partnership** | `EXPLICIT_NEGATIVE` | Cannot marry/register civil partnership (needs Marriage Visa) | **Yes** (Quoted verbatim) | **Yes** (Quoted verbatim) | None (**Zero negative overreach**) |
| **S3-14** | Requirement: Proof of Departure | `TEXT` | Must show you will leave UK at end of visit | **Yes** (Exact rule quoted) | **Yes** (Exact rule quoted) | None (Retained) |
| **S3-15** | Requirement: Sufficient Funds | `TEXT` | Able to support self and dependants during trip | **Yes** (Exact rule quoted) | **Yes** (Exact rule quoted) | None (Retained) |
| **S3-16** | Requirement: Return Travel Funding | `TEXT` | Able to pay for return or onward journey | **Yes** (Exact rule quoted) | **Yes** (Exact rule quoted) | None (Retained) |

---

## 3. Key Empirical Findings on S3

1. **Preservation of Four Selected Negative Constraints (RQ4)**:
   - In Pilot 01 (commercial retail product listings on Daraz), when explicit negative claims were absent from the page, both agents committed severe **negative overreach** (Gap 3)—confidently declaring that unlisted tablet models were physically incompatible simply because they were not selectable in a drop-down menu.
   - On Site S3 (Gov.uk), where negative constraints are explicitly codified under an unambiguous semantic heading (`"You cannot:"`), both agents reported the four selected prohibitions:
     - Neither agent generalized beyond the four stated prohibitions.
     - Both models quoted the exact legal caveats (e.g., noting the exception for permitted paid engagements, and cross-referencing the requirement for a Marriage Visitor visa).
   - These cases are consistent with explicit wording helping the agents preserve listed prohibitions. They do not isolate wording as the cause of the difference between the retail and visa cases.

2. **High Reported Retention on the Selected Semantic Markup Items (16/16 per agent in the existing case coding)**:
   - Gov.uk utilizes strict semantic HTML (headings, ordered lists, markdown-like callout blocks) without client-side hydration barriers or graphical text embedding.
   - Both agent reports covered the 16 selected items under the case's original coding. This is not a cross-site accuracy estimate.

3. **Ground-Truth Fee Schedule Calibration**:
   - The pre-registration inventory matrix noted a baseline fee of `£120` from prior documentation.
   - Both agents live-inspected the canonical page and reported the recently updated statutory fee: **`£135`** (`<p>A Standard Visitor visa costs £135 for up to 6 months.</p>`).
   - Both agents successfully avoided stale training-data contamination by strictly reporting the live ground-truth figure displayed on the page.

4. **Extreme Tool and Cost Efficiency**:
   - OpenCode/Qwen resolved the entire 4-question statutory inquiry in **13 seconds** using 2 tool calls and costing **$0.006316**.
