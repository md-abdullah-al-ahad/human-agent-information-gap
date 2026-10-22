# S4: Supabase Pricing — Paired Agent & Tool Trace Audit (Track A)

**Status:** Completed empirical evaluation for S4 (Track A Live Browsing).  
**Evaluation Date:** 2026-10-19.  
**Evaluated Agents:**
1. **OpenCode / Qwen 3.8 27B Medium** (OpenRouter)
2. **Antigravity CLI / Gemini 3.8 Flash Medium** (Google)
**Tooling Environment:** Playwright MCP (OpenCode) / Web fetch & text parser (Antigravity).

---

## 1. Provenance and Runtime Metadata

| Measure | OpenCode / Qwen 3.8 27B | Antigravity / Gemini 3.8 Flash |
|---|---|---|
| **Session ID** | `ses_eaf4082f1ffehnVumHlAmRY9oR` | `ea109128-6a64-4c4a-bc2a-2c42bc2edd34` |
| **Execution Timestamp** | 2026-10-19 02:41:29 Asia/Dhaka | 2026-10-19 02:41:30 Asia/Dhaka |
| **Retrieval Tool Strategy** | Playwright MCP: `browser_navigate` (1), `browser_snapshot` (1) | `read_url_content` (2), python parsing (1) |
| **Additional Tools Invoked** | None (pure single-pass accessibility snapshot) | Worklog update, file reads |
| **Session Cost** | **$0.014487** (OpenRouter billed cost) | Billed per Google subscription (not exposed in export) |
| **Token Usage** | Input: 35,546; Output: 503; Reasoning: 823 | Input: ~46,000; Output: ~2,800 |
| **Raw Answer File** | [`opencode-qwen-user-exported-answer.md`](opencode-qwen-user-exported-answer.md) | [`antigravity-gemini-user-exported-answer.md`](antigravity-gemini-user-exported-answer.md) |
| **Full Session JSON** | [`opencode-qwen-session.json`](opencode-qwen-session.json) | [`antigravity-gemini-session.json`](antigravity-gemini-session.json) |

---

## 2. Evaluation Against Researcher-Annotated Reference (22 Items)

| Item ID | Target Information Item | Modality Surface | Human Ground Truth | Qwen Retrieved & Reported | Gemini Retrieved & Reported | Information Gap Classification |
|---|---|---|---|---|---|---|
| **S4-01** | Free Tier Base Price | `TEXT` | `$0 / month` | **Yes** (`$0/month`) | **Yes** (`$0 / month`) | None (Retained) |
| **S4-02** | Free Tier DB Storage | `TEXT` | `500 MB database size` | **Yes** (`500 MB`) | **Yes** (`500 MB`) | None (Retained) |
| **S4-03** | Free Tier Compute / RAM | `TEXT` | `Shared CPU • 500 MB RAM` | **Yes** (`Shared CPU • 500 MB RAM`) | **Yes** (`Shared CPU • 500 MB RAM`) | None (Retained) |
| **S4-04** | Free Tier Egress Quota | `TEXT` | `5 GB egress` | **Yes** (`5 GB`) | **Yes** (`5 GB`) | None (Retained) |
| **S4-05** | Free Tier Cached Egress | `TEXT` | `5 GB cached egress` | **Yes** (`5 GB cached egress`) | **Yes** (`5 GB cached egress`) | None (Retained) |
| **S4-06** | Free Tier File Storage | `TEXT` | `1 GB file storage` | **Yes** (`1 GB`) | **Yes** (`1 GB`) | None (Retained) |
| **S4-07** | Free Tier MAU Limit | `TEXT` | `50,000 monthly active users` | **Yes** (Captured in tree) | **Yes** (Captured in tree) | None (Retained) |
| **S4-08** | **Free Auto-Pause Rule** | `TEXT` | Paused after 1 week inactivity | **Yes** (Exact rule quoted) | **Yes** (Exact rule quoted) | None (Critical constraint retained) |
| **S4-09** | **Free Project Limit** | `TEXT` | Limit of 2 active projects | **Yes** (`Limit of 2 active projects`) | **Yes** (`2 active projects`) | None (Critical constraint retained) |
| **S4-10** | Pro Tier Base Price | `TEXT` | `$25 / month` (From $25/mo) | **Yes** (`From $25/month`) | **Yes** (`$25 / month`) | None (Retained) |
| **S4-11** | Pro Included Projects | `TEXT` | First project included | **Yes** (`First project included`) | **Yes** (`1 project / compute credits`) | None (Retained) |
| **S4-12** | Pro Extra Project Fee | `TEXT` | `$10/mo per extra project` | **Yes** (`Additional from $10/mo`) | **Yes** (`$10/month per additional`) | None (Retained) |
| **S4-13** | Pro Included DB Storage | `TEXT` | `8 GB disk size per project` | **Yes** (`8 GB disk size per project`) | **Yes** (`8 GB disk size per project`) | None (Retained) |
| **S4-14** | **Pro DB Overage Rate** | `TEXT` | `$0.125 per GB` | **Yes** (`$0.125 per GB`) | **Yes** (`$0.125 per GB`) | None (Retained) |
| **S4-15** | Pro Included Egress | `TEXT` | `250 GB egress` | **Yes** (`250 GB`) | **Yes** (`250 GB`) | None (Retained) |
| **S4-16** | **Pro Egress Overage Rate** | `TEXT` | `$0.09 per GB` (cached: `$0.03/GB`) | **Yes** (`$0.09 per GB`, cached `$0.03`) | **Yes** (`$0.09 per GB`, cached `$0.03`) | None (Retained) |
| **S4-17** | Pro Included File Storage | `TEXT` | `100 GB file storage` | **Yes** (`100 GB`) | **Yes** (`100 GB`) | None (Retained) |
| **S4-18** | **Pro Storage Overage Rate** | `TEXT` | `$0.0213 per GB` | **Yes** (`$0.0213 per GB`) | **Yes** (`$0.0213 per GB`) | None (Retained) |
| **S4-19** | Pro Backup Retention | `TEXT` | Daily backups for 7 days | **Yes** (`7 days`) | **Yes** (`7 days`, noted PITR add-on) | None (Retained) |
| **S4-20** | Pro Log Retention | `TEXT` | 7-day log retention | **Yes** (`7-day log retention`) | **Yes** (`7 days`) | None (Retained) |
| **S4-21** | Pro Add-ons (PITR / Log Drains) | `TEXT` | PITR / Log Drains ($60-$100/mo) | **Yes** (Verified in matrix) | **Yes** (Quoted PITR $100/mo) | None (Retained) |
| **S4-22** | Matrix Accordions | `DYNAMIC` | Collapsible rows below cards | **Yes** (Traversed in snapshot) | **Yes** (Traversed in markdown) | None (Retained) |

---

## 3. Key Empirical Findings on S4

1. **High Quantitative Density Extraction (22/22 Items, 100% Retention)**:
   - Technical SaaS pricing pages present dense numerical matrices with multiple tiers, quantitative caps, rate cards, and sub-bullets.
   - Both models extracted 100% of the target figures across both the Free and Pro plans without confusing tier allocations or conflating base quotas with overage fees.

2. **Fine-Grained Technical Disambiguation**:
   - Both models captured fine-grained distinctions present in the DOM:
     - Distinguishing standard network egress (5 GB on Free, 250 GB on Pro, $0.09/GB overage) from cached CDN egress (5 GB on Free, 250 GB on Pro, $0.03/GB overage).
     - Identifying that the Free tier provides `500 MB database size` on `Shared CPU • 500 MB RAM`, whereas Pro provides `8 GB disk size per project`.
     - Identifying the multi-project pricing model: first project included in the $25 base fee, subsequent projects at $10/month.

3. **Inactivity & Usage Constraint Fidelity**:
   - Both agents accurately identified and reported the two critical developer constraints on the Free tier:
     - The automatic pausing rule after **1 week of inactivity**.
     - The hard ceiling of **2 active projects**.

4. **Consistency Across Retrieval Modalities**:
   - OpenCode evaluated the live page through Playwright accessibility snapshot in 31 seconds ($0.0144 cost).
   - Antigravity inspected the page content via `read_url_content` and parsed the structured tables.
   - Both pipelines achieved 100% numerical and categorical parity.
