

I inspected the live page with Playwright. Here are the findings, with citations to page sections:

## 1. Product title, model number, product code

| Item | Value | Source on page |
|---|---|---|
| Full title | **ASUS TUF Gaming A15 FA506NCG Ryzen 7 155 RTX 3050 4GB Graphics 15.6" FHD 144Hz Gaming Laptop** | H1 heading in the product header; also repeated in breadcrumb and Description section |
| Model | **TUF Gaming A15 FA506NCG** | "Key Features" list: `Model: TUF Gaming A15 FA506NCG` |
| MPN | **FA506NCG-HN433W** | "Key Features" list: `MPN: FA506NCG-HN433W`; also in Specification table → Physical Specification → "Part Number / MPN" |
| Product Code | **53826** | Product info table row: `Product Code: 53826` |
| Brand | Asus | Product info table row: `Brand: Asus` |

## 2. Displayed prices

From the product info table and the "Payment Options" section:
- **Price (Cash Discount Price): 144,000৳** — info table `Price: 144,000৳`, and radio option "144,000৳ — Cash Discount Price — Online / Cash Payment" (selected by default)
- **Regular Price: 153,780৳** — info table `Regular Price: 153,780৳`
- FAQ section confirms: "The latest price ... in Bangladesh is 144,000৳"

## 3. Stock availability

- **"In Stock"** — product info table row: `Status: In Stock`. No other stock wording appears on the page.

## 4. Technical specifications (from the Specification tab table)

Note: the page contains **internal inconsistencies** — the "Key Features" box lists different processor/RAM values than the Specification table. I quote both:

- **Processor**
  - Key Features box: `AMD Ryzen 7 8845HS (24MB Cache, Up to 5.1GHz)`
  - Specification table → Processor: `Processor Model: Ryzen 7 155`, `Generation: 100 Series`, `Up to 4.7GHz`, `6-Cores`, `12-Threads`, `CPU Cache: 22MB`
- **Graphics** — Specification table → Graphics: `NVIDIA GeForce RTX 3050 Laptop GPU, Up to 1675MHz at 60W (75W with Dynamic Boost)`, `4GB`, `GDDR6` (Key Features matches: "RTX 3050 4GB GDDR6, Up to 1675MHz")
- **RAM** — Specification table → Memory: `8GB (SO-DIMM)`, `DDR5`, `Bus Speed: 4800Mhz`, `Removable: Yes`, `2 slots`, `Max RAM: up to 64GB`. Key Features box instead says `8GB DDR5-5600` (conflicts with the 4800MHz table entry)
- **Storage** — Specification table → Storage: `512GB`, `M.2 NVMe PCIe 4.0 SSD`, `Extra M.2 Slot: Yes`, `2x M.2 slots (SATA or NVMe)`
- **Display** — Specification table → Display: `15.6-inch`, `Value IPS-level`, `FHD (1920 x 1080)`, `144Hz`, `16:9, Anti-glare, sRGB 62.5%, NTSC 45%, Adaptive-Sync, Optimus` (Description section adds "250 nits")

## 5. Warranty

- **"02 years International Limited Warranty (Battery 1 year)"** — Specification table → Warranty section (`Warranty Details` row). Also stated in the Description text: "The ASUS TUF Gaming A15 ... comes with 02 years International Limited Warranty (Battery 1 year)." No other warranty terms are given on this page.

## 6. Payment / EMI / delivery promotions

From the "Payment Options" section and surrounding elements:
- **Cash:** 144,000৳ — "Cash Discount Price — Online / Cash Payment" (radio option 1)
- **EMI:** 12,815৳/month — "Regular Price: 153,780৳ — 0% EMI for up to 12 Months***" (radio option 2). Full EMI terms are not detailed on the page (only a footer link "EMI Terms" exists)
- **Star Points:** "2X for Limited Time" badge showing **450 Star Points**
- **10.10 promo banner** — a promotional image (alt "Product Page | 10.10") linking to the `/10-10` campaign page; no promo text beyond the image on this page
- **Delivery:** No delivery fee, shipping time, or delivery promotion is stated anywhere on this product page (only a generic footer link "Online Delivery")

Not stated on the page: exact delivery time/fee, EMI provider names, and any condition of the "***" EMI footnote.