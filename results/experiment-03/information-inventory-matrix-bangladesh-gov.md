# Pre-Registered Information Inventory Matrix: Bangladesh National Portal (Site ID: BD-GV01)

- **Domain Category**: Public Administration & Statutory Portals
- **Platform Name**: Bangladesh National Portal (বাংলাদেশ জাতীয় তথ্য বাতায়ন)
- **Canonical URL**: `https://bangladesh.gov.bd`
- **Capture Timestamp**: 2026-10-19T11:32:19Z
- **Fullpage Visual Screenshot**: `data/stage-4/screenshots/bd-gv01-fullpage.png` (SHA-256: `01f47375e0f66b77242ba4cb178d8a1bfcf51b0333d06eec73dbbe00da5a1b32`, 1280 x 2693 px)
- **Raw Machine DOM Snapshot**: `data/stage-4/raw/bd-gv01-dom.html` (SHA-256: `f88cec77e4f0cc64f331fe278631c3bf1e0b5ef358c5c7ce1a547b744d081f9a`, 139,768 bytes)

---

## 20 Pre-Registered Ground-Truth Inventory Items

| Item ID | Target Information Unit | Expected Value / Ground Truth | Modality & Physical Location | DOM Presence | Visual Visibility | Grounding Coordinates / DOM Selector |
|---|---|---|---|---|---|---|
| `GV-01` | Portal Main Header Title | "বাংলাদেশ জাতীয় তথ্য বাতায়ন" | Text / Header Branding | Present | Fully Visible | Header title adjacent to national crest |
| `GV-02` | Header Current Date Display | "১৯ অক্টোবর ২০২৬" | Text / Top utility bar | Present | Fully Visible | Top left bar date text |
| `GV-03` | Header Search Input Placeholder | "এখানে খুঁজুন..." | DOM Attribute / Input placeholder | Present (`placeholder="এখানে খুঁজুন..."`) | Fully Visible | `input.search-input` placeholder |
| `GV-04` | Food Safety Popup Modal Main Title | "পোড়া তেল ব্যবহার করবেন না" | In-Image Graphic (Trapped Raster Pixel) | Absent (`alt="Image"`) | Fully Visible (Top Modal) | `img.popup-widget-image` top header banner |
| `GV-05` | Food Safety Popup Issuing Authority & URL | "বাংলাদেশ নিরাপদ খাদ্য কর্তৃপক্ষ" & "www.bfsa.gov.bd" | In-Image Graphic (Trapped Raster Pixel) | Absent (`alt="Image"`) | Fully Visible (Top Modal) | `img.popup-widget-image` bottom branding |
| `GV-06` | Food Safety Popup Medical Health Risks | "স্ট্রোক ও হৃদরোগ" (Stroke and Heart Disease from trans fats) | In-Image Graphic (Trapped Raster Pixel) | Absent (`alt="Image"`) | Fully Visible (Top Modal) | `img.popup-widget-image` panel 2 |
| `GV-07` | Food Safety Popup Recommended Alternative | "ছেঁকে তরকারিতে ব্যবহার করতে পারেন" (Strain and reuse in curry) | In-Image Graphic (Trapped Raster Pixel) | Absent (`alt="Image"`) | Fully Visible (Top Modal) | `img.popup-widget-image` panel 4 |
| `GV-08` | Hero Banner Advertised Applet: GPF Calculator | "ভবিষ্য তহবিল ক্যালকুলেটর" | In-Image Graphic (Trapped Raster Pixel in Hero Slider) | Absent (`alt="MyGov Banner"`) | Fully Visible (Hero Carousel) | Slider image `277dea5e...jpeg` top-center applet |
| `GV-09` | Hero Banner Advertised Applet: Inheritance Calculator | "উত্তরাধিকার" ("উত্তরাধিকার বাংলা - এক ক্লিকেই সম্পত্তির হিসাব") | In-Image Graphic (Trapped Raster Pixel in Hero Slider) | Absent (`alt="MyGov Banner"`) | Fully Visible (Hero Carousel) | Slider image `277dea5e...jpeg` right applet |
| `GV-10` | Administrative Counter: Ministries & Divisions | "৫৭" (57) মন্ত্রণালয় ও বিভাগ | Structured Counter Bar | Present | Fully Visible | `.all-site-count-widget-value` item 1 |
| `GV-11` | Administrative Counter: Upazilas | "৫০০" (500) উপজেলা | Structured Counter Bar | Present | Fully Visible | `.all-site-count-widget-value` item 6 |
| `GV-12` | Administrative Counter: Union Parishads | "৪৫৬৮" (4568) ইউনিয়ন | Structured Counter Bar | Present | Fully Visible | `.all-site-count-widget-value` item 7 |
| `GV-13` | Government Services Widget Active Default Tab | "জনপ্রিয় সেবা" (Popular Services) | Interactive Tab Bar | Present | Fully Visible | Active tab in `.national-portal-services-widget` |
| `GV-14` | Popular Services Grid: Service Card 8 | "পাসপোর্ট, ভিসা ও ইমিগ্রেশন" | Service Grid Card | Present | Fully Visible | Service item #8 in default tab |
| `GV-15` | Popular Services Grid: Fold-Hidden Service Item | "ইউটিলিটি বিল" | Dynamic Fold-Hidden Item | Present in DOM | Hidden behind "আরো দেখুন ↓" | Service item #10 in default tab |
| `GV-16` | Emergency Helpline 1 | "৩৩৩" -> সরকারি তথ্য ও সেবা | Sidebar Helpline List | Present | Fully Visible | Helpline item 1 |
| `GV-17` | Emergency Helpline 4 | "১৬১০৭" -> বিআরটিএ সার্ভিস পোর্টাল (বিএসপি) | Sidebar Helpline List | Present | Fully Visible | Helpline item 4 |
| `GV-18` | Emergency Helpline Fold-Hidden Item | "১৬১২২" -> স্মার্ট ভূমি সেবা | Dynamic Fold-Hidden Item | Present in DOM | Hidden behind `#toggle-hotlines` | Helpline item 9 (requires expansion) |
| `GV-19` | Photo Gallery Item 4 Caption / Visual Subject | "নৌকা বাইচ" (Traditional Boat Race) | Media Gallery | Present (`alt="নৌকা বাইচ"`) | Fully Visible | Gallery item 4 |
| `GV-20` | Footer Implementation Partners Cluster | a2i, Cabinet Division, ICT Division, UNDP | Footer Partner Composite Graphic | Partial (DOM has only `alt="a2i"`) | Fully Visible | `img[src*="a2iset.png"]` contains 4 logos |
