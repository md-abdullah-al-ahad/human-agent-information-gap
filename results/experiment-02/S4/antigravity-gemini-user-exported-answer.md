Based on Supabase's official pricing page ([https://supabase.com/pricing](https://supabase.com/pricing)), here are the answers comparing the Free and Pro plans:

---

### 1. Monthly Base Prices and Included Projects

- **Free Plan**:
  - **Base Price**: **$0 / month** (or "from $0/month").
  - **Included Projects**: **2 active projects** are included. You can create up to 2 active projects, with an unlimited number of paused projects.
- **Pro Plan**:
  - **Base Price**: **$25 / month** (or "from $25/month").
  - **Included Projects**: Includes **$10/month in compute credits**, which covers **1 project** on a Micro compute instance. Additional projects are billed for their own compute instances (e.g., $10/month for each additional Micro instance).

---

### 2. Storage and Bandwidth Egress Limits

| Metric | Free Plan | Pro Plan |
| :--- | :--- | :--- |
| **Database Storage** | **500 MB** database size per project (Shared CPU • 500 MB RAM) | **8 GB** disk size per project included (General Purpose disk) |
| **File Storage** | **1 GB** file storage included (Max file upload size: 50 MB) | **100 GB** file storage included (Max file upload size: 500 GB) |
| **Bandwidth Egress** | **5 GB** egress included (+ **5 GB** cached egress) | **250 GB** egress included (+ **250 GB** cached egress) |

---

### 3. Pro Plan Overage Rates (Extra Charges)

When spend caps are turned off on the Pro plan, extra usage beyond the included quotas is billed at the following rates:

- **Additional Database Storage**:
  - **General Purpose Disk**: **$0.125 per GB** (beyond the 8 GB per project included).
  - *(Note: High Performance disk is also listed at $0.195 per GB).*
- **Additional File Storage**:
  - **$0.0213 per GB** (beyond the 100 GB included).
- **Additional Bandwidth Egress**:
  - **Egress**: **$0.09 per GB** (beyond the 250 GB included).
  - **Cached Egress**: **$0.03 per GB** (beyond the 250 GB included).

---

### 4. Auto-Pause Rules and Active Project Limits (Free Plan)

- **Auto-Pause Rules**:
  - Free projects are **automatically paused after 1 week of inactivity**.
  - Users may pause and unpause projects manually at any time; there is no limit on the number of paused projects you can maintain.
  - Projects on paid plans are never paused for inactivity.
- **Active Project Limits**:
  - **Limit of 2 active projects**.

---

### 5. Backup Retention and Log Retention Periods (Pro Plan)

- **Backup Retention Period**:
  - **7 days** (Daily backups stored for 7 days).
  - *(Optional add-on: Point-in-Time Recovery / PITR is available for $100 per month per 7 days of retention).*
- **Log Retention Period**:
  - **7 days** (Applies to API & Database logs as well as Auth Audit Logs).

---

Log updated: `/home/abdullah/.agent_worklogs/general/2026-10.log.md`