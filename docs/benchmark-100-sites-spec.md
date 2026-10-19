# Benchmark 100: Multi-Modal Human–Agent Information Gap Benchmark

**Status:** Specification & Execution Protocol  
**Benchmark Scope:** 100 Real-World Web Platforms across 10 Strategic Domains  
**Primary Research Goal:** Quantify the Information Loss Pipeline (`Human Surface -> Tool-Exposed -> Agent-Retrieved -> Output`) and benchmark tool ablation (With Playwright vs. Without Playwright) across multi-modal frontier models.

---

## 1. The 10 Strategic Domains (10 Sites per Domain = 100 Total)

The benchmark is stratified into 10 balanced operational domains covering diverse web architectures (SSR, CSR, Angular, React, Vue, client-side SPAs, Cloudflare-protected, heavy graphical banner layouts):

1. **Quick-Commerce & Grocery Delivery**: High-frequency essentials, tiered delivery fee matrices, localized delivery coverage, perishable return limits.
2. **Multi-Vendor E-Commerce Marketplaces**: Multi-tier variant selectors, seller-brand conflicts, promotional voucher carousels, payment partner cashbacks.
3. **Transit, Aviation & Intercity Rail**: Multi-step route finders, seat selection maps, temporal cancellation blackout windows, strict passenger prerequisites.
4. **Consumer Electronics & Tech Retail**: Multi-attribute specification matrices, cash vs. card tiered pricing, out-of-stock UI affordance signals.
5. **Banking, Fintech & Mobile Wallets**: Transaction fee schedules, daily limit tables, security badges, accepted merchant sprite grids.
6. **Healthcare, Hospitals & Telemedicine**: Doctor department taxonomies, visiting hour constraints, appointment booking affordances, service scopes.
7. **Statutory Public Sector & Government**: Statutory eligibility rules, structured negative legal constraints (`"You cannot"`), public fee schedules.
8. **Classifieds, Recruitment & Real Estate**: C2C unstandardized metadata, salary/price negotiations, regional location filtering.
9. **Education, EdTech & Academic Portals**: Course syllabus hierarchies, enrollment blackout deadlines, prerequisite requirement constraints.
10. **SaaS & Cloud Infrastructure**: Tiered compute pricing matrices, usage-based sliders, plan entitlement limits, enterprise overage rules.

---

## 2. Standardized 5-Point Core Failure Probing Protocol

To ensure rigorous consistency across all 100 platforms, each evaluation targets the known failure modes identified in our exploratory trials:

1. **Probe 1: In-Image Visual Graphics & Trapped Data (Modality 3)**:
   - Extract promotional discounts, partner cashback terms, voucher codes, or entity names rendered inside graphical JPEG/PNG banners or icon sprites lacking accessible `alt` text.
2. **Probe 2: Dynamic Client Hydration (Modality 2 / Gap 1)**:
   - Identify critical service scopes or notification banners rendered exclusively post-hydration via client JavaScript, testing static crawler blindness.
3. **Probe 3: Tabular Structure & Tiered Pricing (Modality 1)**:
   - Parse multi-tier pricing, threshold fee schedules, or specification matrices for exact numeric fidelity.
4. **Probe 4: Explicit Negative Constraints & Temporal Limits (Modality 4 / RQ4)**:
   - Extract explicit exclusion windows, perishable return time limits, or prerequisite prohibitions to test negative overreach and hallucination.
5. **Probe 5: Platform Identity & Direct Contact Grounding**:
   - Verify official customer support hotlines and emails, specifically evaluating resistance to dynamic obfuscation (e.g., Cloudflare email protection).

---

## 3. Four-Arm Factorial Experimental Matrix per Site

Each platform is evaluated across 4 isolated experimental conditions:
1. **Arm 1: OpenCode / Qwen 3.8 27B + Playwright MCP** (Headless browser + dynamic visual evaluation).
2. **Arm 2: Antigravity / Gemini 3.8 Flash + Playwright MCP** (Headless browser + multi-step reasoning).
3. **Arm 3: OpenCode / Qwen 3.8 27B + Static Scraper** (Static HTTP / cURL baseline without browser automation).
4. **Arm 4: Antigravity / Gemini 3.8 Flash + Static Scraper** (Static HTTP / cURL baseline without browser automation).

**Benchmark Dataset Scale:**
- **100 Target Websites**
- **500 to 1,000 Pre-Registered Ground-Truth Items**
- **400 Headless Agent Execution Sessions**
- **2,000 to 4,000 Evaluated Observation Rows**

---

## 4. Multi-Level Self-Evaluation & Verification Harness

To eliminate human and algorithmic errors, every site ingestion and evaluation must pass 5 automated verification gates:

### Gate 1: Network & HTTP Liveness Check
- The target URL must return an HTTP 200 OK status code.
- Must not terminate in a CAPTCHA interstitial or 403 Cloudflare block screen.

### Gate 2: Visual Screenshot Non-Triviality Check
- Screenshot file must exist on disk and be > 50 KB.
- Image resolution must have `width >= 1000 px` and `height >= 800 px`.
- Standard deviation of pixel luminance (RGB variance) must exceed threshold `σ > 15` (rejects solid white or solid black blank frames).

### Gate 3: Machine DOM Integrity Check
- DOM HTML file must exist on disk and be > 10 KB.
- Must contain valid HTML structural tags (`<html`, `<body`, `</html>`).

### Gate 4: Cryptographic Bit-Level Provenance Check
- SHA-256 hashes for both screenshot and DOM must be generated and verified against `data/stage-4/manifest.json`.

### Gate 5: Execution Trace & Provenance Verification
- Every agent session must have a verifiable session ID in `opencode.db` or Antigravity's `.system_generated/logs/transcript.jsonl`.
- Input, cache read, output tokens, latency (seconds), and billed USD cost must be extracted from database rows, never estimated.
