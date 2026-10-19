# Experiment 03 — Information Inventory Matrix: Site BD-01 (Shohoz Bus Tickets)

**Target URL:** `https://www.shohoz.com/bus-tickets/`  
**Platform:** Shohoz (Shohoj Limited)  
**Domain Stratum:** Long-Distance Transit & Online Bus Ticketing (Bangladesh)  
**Visual Capture:** [`data/stage-4/screenshots/shohoz-bus-fullpage.png`](../../data/stage-4/screenshots/shohoz-bus-fullpage.png) (1208 × 6,470 px, SHA-256 `590f6c7cd0a1...`)  
**Raw Static DOM:** [`data/stage-4/raw/shohoz-bus-dom.html`](../../data/stage-4/raw/shohoz-bus-dom.html) (153.2 KB, SHA-256 `6af46bc9e9d9...`)  
**Evaluation Scope:** Paired Tool Ablation — Condition 1 (Without Playwright / Static Fetch) vs. Condition 2 (With Playwright / Headless Browser).

---

## 1. Pre-Registered Ground-Truth Inventory (22 Discrete Items)

| Item ID | Information Category & Fact | Modality Surface | Human-Observable Location | Exposed in Raw Static DOM? | Target Research Check |
|---|---|---|---|---|---|
| **BD1-01** | Platform Identity (`Shohoz` / `Shohoj Limited`) | `TEXT` | Header logo & footer copyright | Yes | Entity identification |
| **BD1-02** | Main Service Heading (`Book & Buy Bus Tickets Online`) | `TEXT` | Main H1 heading above search | Yes | Service scope extraction |
| **BD1-03** | Search Input: Origin (`From` city input) | `DYNAMIC` | Search bar input 1 | Yes (Angular control) | Search affordance |
| **BD1-04** | Search Input: Destination (`To` city input) | `DYNAMIC` | Search bar input 2 | Yes (Angular control) | Search affordance |
| **BD1-05** | Search Input: Journey Date (`Journey Date` picker) | `DYNAMIC` | Search bar input 3 | Yes (Angular control) | Search affordance |
| **BD1-06** | Trip Type Selector (`One Way` vs `Round Way`) | `DYNAMIC` | Radio buttons above search | Yes (Angular control) | Search affordance |
| **BD1-07** | Return Trip Add Button (`+ ADD RETURN TRIP`) | `DYNAMIC` | Button inside search bar | Yes (Angular control) | Search affordance |
| **BD1-08** | Trending Destinations (Chittagong, Dhaka, Rajshahi, Rangpur, Sylhet) | `TEXT` | Destination image cards | Yes | Content extraction |
| **BD1-09** | Featured Operators (Nabil, SR, Shohagh, Royal Coach, Hanif, Soudia, Robi, Green Line) | `TEXT` | Operator logo cards | Yes | Partner roster extraction |
| **BD1-10** | Operator Count Metric (`100+ operators nationwide`) | `TEXT` | Section title & subtext | Yes | Quantitative claim fidelity |
| **BD1-11** | Scale Metrics (`250M+ tickets`, `10M+ users`, `3000+ routes`, `1000+ partners`) | `TEXT` | Value proposition badges | Yes | Multi-metric fidelity |
| **BD1-12** | Customer Support Helpline (`16374`) | `TEXT` | Header & FAQ section | Yes | Contact affordance extraction |
| **BD1-13** | Helpline Operating Hours (`7 AM - 11 PM`) | `TEXT` | Subtext below 16374 in header | Yes | Temporal limit extraction |
| **BD1-14** | Support Email (`info@shohoz.com`) | `TEXT` | FAQ answer 5 | Yes | Contact affordance extraction |
| **BD1-15** | Purchase Channels (Website, Android/iOS App, Helpline 16374) | `TEXT` | FAQ Accordion 1 | Yes | Multi-channel extraction |
| **BD1-16** | Purchase Time Window (No time limit online; helpline 7 AM - 11 PM) | `TEXT` | FAQ Accordion 2 | Yes | Policy constraint extraction |
| **BD1-17** | Cancellation/Migration Time Limit (`12/24 hours before departure`) | `TEXT` | FAQ Accordion 3 | Yes | Policy constraint extraction |
| **BD1-18** | **Explicit Negative Blackout: Cancellation Calculation (`excluding 11 PM to 7 AM`)** | `EXPLICIT_NEGATIVE` | FAQ Accordion 3 | Yes | **Negative constraint fidelity (RQ4)** |
| **BD1-19** | **Mandatory Migration Rule (Must call strictly from booking phone number)** | `TEXT` | FAQ Accordion 3 | Yes | Critical operational prerequisite |
| **BD1-20** | **Refund Schedule: bKash & Nagad (`Maximum of 5-7 working days`)** | `TEXT` | FAQ Accordion 5 | Yes | Quantitative policy split |
| **BD1-21** | **Refund Schedule: Cards & Internet Banking (`Maximum of 7-10 working days`)** | `TEXT` | FAQ Accordion 5 | Yes | Quantitative policy split |
| **BD1-22** | Unified Login Scope (Single Shohoz account for `Bus, Air, and Park`) | `TEXT` | Green notification banner | Yes | Cross-service authentication rule |

---

## 2. Experimental Tool Ablation Protocol

We test the exact same user prompt across two distinct agent conditions:

### Condition 1: Without Playwright (Static Baseline)
- **Agent Capability**: Restricted to static HTTP GET / `read_url_content` / cURL.
- **Hypothesis**: The agent will extract basic static text, but will be blind to dynamic state, cannot execute interactive form searches, and will be measured for context window and token efficiency.

### Condition 2: With Playwright (Headless Browser)
- **Agent Capability**: Full Playwright MCP (`browser_navigate`, `browser_snapshot`, `browser_evaluate`).
- **Hypothesis**: The agent will capture rendered accessibility trees and dynamic states, but will incur a 3x to 10x token bloat and significantly higher latency and API cost.

---

## 3. Resource & Cost Metrics Tracked
- **Total Input Tokens**
- **Total Output & Reasoning Tokens**
- **Billed Cost (USD via OpenRouter)**
- **Wall-Clock Latency (seconds)**
- **Tool Calls Count**
- **Information Yield per 1,000 Tokens**
