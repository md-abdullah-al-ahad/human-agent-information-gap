# Pre-Registered Information Inventory Matrix: US-Bangla Airlines (Site ID: BD-TR03)

- **Domain Category**: Transit, Aviation & Intercity Rail
- **Platform Name**: US-Bangla Airlines
- **Canonical URL**: `https://usbair.com`
- **Capture Timestamp**: 2026-10-19T12:23:50Z
- **Fullpage Visual Screenshot**: `data/stage-4/screenshots/bd-tr03-fullpage.png` (SHA-256: `ae78ad793638d08915e8da1fb443f14e414c22a7f5c907b227c8a6f44d18ecf5`, 1333 x 3866 px)
- **Raw Machine DOM Snapshot**: `data/stage-4/raw/bd-tr03-dom.html` (SHA-256: `df2a017b6356ae3b610c1f540707ecf6ec1086036a19f2a2491fe2198031ba0d`, 102,426 bytes)

---

## 20 Pre-Registered Ground-Truth Inventory Items

| Item ID | Target Information Unit | Expected Value / Ground Truth | Modality & Physical Location | DOM Presence | Visual Visibility | Grounding Coordinates / DOM Selector |
|---|---|---|---|---|---|---|
| `TR03-01` | Origin Airport Default Selection | `Dhaka (DAC)` / `Hazrat Shahjalal International Airport` | UI Input / Booking Engine | Present | Fully Visible | From input field in flight search widget |
| `TR03-02` | Flight Search CTA Button Text | `Search Flights` | Button UI / Booking Engine | Present | Fully Visible | Red button with airplane icon |
| `TR03-03` | Default Passenger & Cabin Class | `1 Passenger, Economy` | UI Dropdown / Booking Engine | Present | Fully Visible | Passenger selection trigger |
| `TR03-04` | Mastercard Popup Domestic Promo Code | `USBA15` (15% OFF) | In-Image Graphic (Trapped Raster Pixel) | Absent (`aria-label="US-Bangla Master Card Offer"`) | Fully Visible (Modal) | Left coupon ticket inside `mastercard-offer-popup-web.jpg` |
| `TR03-05` | Mastercard Popup International Promo Code | `USBAIN10` (10% OFF) | In-Image Graphic (Trapped Raster Pixel) | Absent | Fully Visible (Modal) | Right coupon ticket inside `mastercard-offer-popup-web.jpg` |
| `TR03-06` | Mastercard Popup Grand Prize Campaign | `Couple Holiday in Kuala Lumpur!` | In-Image Graphic (Trapped Raster Pixel) | Absent | Fully Visible (Modal) | Red text inside `mastercard-offer-popup-web.jpg` |
| `TR03-07` | Mastercard Popup Domestic Free Return Tickets | `Cox's Bazar \| Sylhet \| Chattogram` | In-Image Graphic (Trapped Raster Pixel) | Absent | Fully Visible (Modal) | Subtitle inside `mastercard-offer-popup-web.jpg` |
| `TR03-08` | Mastercard Popup Campaign Validity | `Till 31st October 2026` (`*T&C Apply`) | In-Image Graphic (Trapped Raster Pixel) | Absent | Fully Visible (Modal) | Bottom line inside `mastercard-offer-popup-web.jpg` |
| `TR03-09` | Mastercard Graphic Cardholder Name | `SABRINA ISLAM` | In-Image Graphic (Trapped Raster Pixel) | Absent | Fully Visible (Modal) | Stamped on black card graphic in popup |
| `TR03-10` | Sky Star Loyalty Program 4 Tier Names | `Silver`, `Gold`, `Platinum`, `Titanium` | In-Image Graphic (Trapped Raster/Vector) | Absent (`alt=""`) | Fully Visible | 4 star badge circles in `Join-Sky-Star.png` |
| `TR03-11` | Sky Star Loyalty Program Heading | `Join Sky Star` | Text / Loyalty Header | Present | Fully Visible | `h4: Join Sky Star` |
| `TR03-12` | Vacation Banner Main Headline | `Enjoy your favorite holiday destination and Earn Miles!` | Text / Hero Banner | Present | Fully Visible | Vacation promo section headline |
| `TR03-13` | Vacation Banner Action Button | `Make Memories` | Button UI / Vacation Section | Present | Fully Visible | White button in vacation promo banner |
| `TR03-14` | Destination Grid Origin City Default | `Dhaka` | UI Input / Auto-complete | Present (`value="Dhaka"`) | Fully Visible | `input#auto_com` |
| `TR03-15` | Kolkata Destination Moniker | `City of Joy` ("Book Your Flight to the City of Joy") | Text / Destination Card | Present | Fully Visible | Kolkata card subtitle |
| `TR03-16` | Guangzhou Destination Moniker | `City of Flowers` ("Book Your Flight to the City of Flowers") | Text / Destination Card | Present | Fully Visible | Guangzhou card subtitle |
| `TR03-17` | Kuala Lumpur Destination Moniker | `cosmopolitan metropolis` ("Book Your Flight to the cosmopolitan metropolis") | Text / Destination Card | Present | Fully Visible | Kuala Lumpur card subtitle |
| `TR03-18` | Special Offers Subscription Input Placeholder | `Email Address` (with `Subscribe` button) | Form Input / Footer | Present | Fully Visible | Subscription input field |
| `TR03-19` | Mobile App Value Proposition | `Book and manage your flight & Get exclusive discounts` | Text / App Footer Card | Present | Fully Visible | Under `US-Bangla Airlines App` |
| `TR03-20` | Official Footer Copyright Notice | `© 2026 US-Bangla Airlines. All rights reserved.` | Text / Legal Footer | Present | Fully Visible | Footer bottom line |
