import csv

rows = [
    # BD-QC02-01
    ("BD-QC02-01", "BD-QC02", "Notification Modal Heading (Get notifications from Shwapno?)", "UI_MODAL", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-01", "BD-QC02", "Notification Modal Heading (Get notifications from Shwapno?)", "UI_MODAL", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-01", "BD-QC02", "Notification Modal Heading (Get notifications from Shwapno?)", "UI_MODAL", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-01", "BD-QC02", "Notification Modal Heading (Get notifications from Shwapno?)", "UI_MODAL", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-02
    ("BD-QC02-02", "BD-QC02", "Notification Primary Button (Yes in bg-yellow vs No)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-02", "BD-QC02", "Notification Primary Button (Yes in bg-yellow vs No)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-02", "BD-QC02", "Notification Primary Button (Yes in bg-yellow vs No)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-02", "BD-QC02", "Notification Primary Button (Yes in bg-yellow vs No)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-03
    ("BD-QC02-03", "BD-QC02", "Hero Banner Campaign Title (স্বপ্ন অনলাইন পূজার সাশ্রয়)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-03", "BD-QC02", "Hero Banner Campaign Title (স্বপ্ন অনলাইন পূজার সাশ্রয়)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Analysis)", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-03", "BD-QC02", "Hero Banner Campaign Title (স্বপ্ন অনলাইন পূজার সাশ্রয়)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-03", "BD-QC02", "Hero Banner Campaign Title (স্বপ্ন অনলাইন পূজার সাশ্রয়)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-04
    ("BD-QC02-04", "BD-QC02", "Puja Promo Code 1 Details (৬% ডিসকাউন্ট, PUJA6)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-04", "BD-QC02", "Puja Promo Code 1 Details (৬% ডিসকাউন্ট, PUJA6)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Analysis)", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-04", "BD-QC02", "Puja Promo Code 1 Details (৬% ডিসকাউন্ট, PUJA6)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-04", "BD-QC02", "Puja Promo Code 1 Details (৬% ডিসকাউন্ট, PUJA6)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-05
    ("BD-QC02-05", "BD-QC02", "Puja Promo Code 2 Details (৭% ডিসকাউন্ট, PUJA7)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-05", "BD-QC02", "Puja Promo Code 2 Details (৭% ডিসকাউন্ট, PUJA7)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Analysis)", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-05", "BD-QC02", "Puja Promo Code 2 Details (৭% ডিসকাউন্ট, PUJA7)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-05", "BD-QC02", "Puja Promo Code 2 Details (৭% ডিসকাউন্ট, PUJA7)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-06
    ("BD-QC02-06", "BD-QC02", "Value Pillar 1: Delivery (60 mins delivery, Free shipping over 1500Tk)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-06", "BD-QC02", "Value Pillar 1: Delivery (60 mins delivery, Free shipping over 1500Tk)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-06", "BD-QC02", "Value Pillar 1: Delivery (60 mins delivery, Free shipping over 1500Tk)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-06", "BD-QC02", "Value Pillar 1: Delivery (60 mins delivery, Free shipping over 1500Tk)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-07
    ("BD-QC02-07", "BD-QC02", "Value Pillar 2: Exchange (Authorized Products, within 30 days for an exchange)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-07", "BD-QC02", "Value Pillar 2: Exchange (Authorized Products, within 30 days for an exchange)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-07", "BD-QC02", "Value Pillar 2: Exchange (Authorized Products, within 30 days for an exchange)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-07", "BD-QC02", "Value Pillar 2: Exchange (Authorized Products, within 30 days for an exchange)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-08
    ("BD-QC02-08", "BD-QC02", "Value Pillar 3: Support (Customer Service Support, 8am to 10pm)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-08", "BD-QC02", "Value Pillar 3: Support (Customer Service Support, 8am to 10pm)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-08", "BD-QC02", "Value Pillar 3: Support (Customer Service Support, 8am to 10pm)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-08", "BD-QC02", "Value Pillar 3: Support (Customer Service Support, 8am to 10pm)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-09
    ("BD-QC02-09", "BD-QC02", "Value Pillar 4: Payment (Flexible Payments, Pay with multiple credit cards)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-09", "BD-QC02", "Value Pillar 4: Payment (Flexible Payments, Pay with multiple credit cards)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-09", "BD-QC02", "Value Pillar 4: Payment (Flexible Payments, Pay with multiple credit cards)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-09", "BD-QC02", "Value Pillar 4: Payment (Flexible Payments, Pay with multiple credit cards)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-10
    ("BD-QC02-10", "BD-QC02", "Fast Category Tile 1 (Eggs)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-10", "BD-QC02", "Fast Category Tile 1 (Eggs)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-10", "BD-QC02", "Fast Category Tile 1 (Eggs)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-10", "BD-QC02", "Fast Category Tile 1 (Eggs)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-11
    ("BD-QC02-11", "BD-QC02", "Fast Category Tile 3 (Soft Drinks)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-11", "BD-QC02", "Fast Category Tile 3 (Soft Drinks)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-11", "BD-QC02", "Fast Category Tile 3 (Soft Drinks)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-11", "BD-QC02", "Fast Category Tile 3 (Soft Drinks)", "UI_TILE", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-12
    ("BD-QC02-12", "BD-QC02", "Egg Loose Price & MOQ (৳12.75, Min. 12)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-12", "BD-QC02", "Egg Loose Price & MOQ (৳12.75, Min. 12)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-12", "BD-QC02", "Egg Loose Price & MOQ (৳12.75, Min. 12)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-12", "BD-QC02", "Egg Loose Price & MOQ (৳12.75, Min. 12)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-13
    ("BD-QC02-13", "BD-QC02", "Alu (Potato) Discount (৳25, ৳5 OFF, original ৳30)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-13", "BD-QC02", "Alu (Potato) Discount (৳25, ৳5 OFF, original ৳30)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-13", "BD-QC02", "Alu (Potato) Discount (৳25, ৳5 OFF, original ৳30)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-13", "BD-QC02", "Alu (Potato) Discount (৳25, ৳5 OFF, original ৳30)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-14
    ("BD-QC02-14", "BD-QC02", "ACI Pure Salt 1kg Price (৳42)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-14", "BD-QC02", "ACI Pure Salt 1kg Price (৳42)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-14", "BD-QC02", "ACI Pure Salt 1kg Price (৳42)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-14", "BD-QC02", "ACI Pure Salt 1kg Price (৳42)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-15
    ("BD-QC02-15", "BD-QC02", "Masala Tea Weekday Deal (Fresh Premium Masala Tea 50gm, ৳95, ৳15 OFF)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-15", "BD-QC02", "Masala Tea Weekday Deal (Fresh Premium Masala Tea 50gm, ৳95, ৳15 OFF)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-15", "BD-QC02", "Masala Tea Weekday Deal (Fresh Premium Masala Tea 50gm, ৳95, ৳15 OFF)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-15", "BD-QC02", "Masala Tea Weekday Deal (Fresh Premium Masala Tea 50gm, ৳95, ৳15 OFF)", "PRODUCT_CARD", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-16
    ("BD-QC02-16", "BD-QC02", "Himalaya Section Title (Refresh with Himalaya)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-16", "BD-QC02", "Himalaya Section Title (Refresh with Himalaya)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-16", "BD-QC02", "Himalaya Section Title (Refresh with Himalaya)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-16", "BD-QC02", "Himalaya Section Title (Refresh with Himalaya)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-17
    ("BD-QC02-17", "BD-QC02", "Dhaka Coverage Outlets (Dhaka, 290 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-17", "BD-QC02", "Dhaka Coverage Outlets (Dhaka, 290 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-17", "BD-QC02", "Dhaka Coverage Outlets (Dhaka, 290 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-17", "BD-QC02", "Dhaka Coverage Outlets (Dhaka, 290 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-18
    ("BD-QC02-18", "BD-QC02", "Gazipur Coverage Outlets (Gazipur, 69 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-18", "BD-QC02", "Gazipur Coverage Outlets (Gazipur, 69 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-18", "BD-QC02", "Gazipur Coverage Outlets (Gazipur, 69 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-18", "BD-QC02", "Gazipur Coverage Outlets (Gazipur, 69 outlets)", "QUANTITATIVE", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-19
    ("BD-QC02-19", "BD-QC02", "Support Hotline & Email (16469 8am-10pm Everyday, queries@acilogistics.net)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-19", "BD-QC02", "Support Hotline & Email (16469 8am-10pm Everyday, queries@acilogistics.net)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-19", "BD-QC02", "Support Hotline & Email (16469 8am-10pm Everyday, queries@acilogistics.net)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-19", "BD-QC02", "Support Hotline & Email (16469 8am-10pm Everyday, queries@acilogistics.net)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-QC02-20
    ("BD-QC02-20", "BD-QC02", "Operating Entity & Copyright (ACI SHWAPNO E-COMMERCE LIMITED, Copyright © 2026)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-QC02-20", "BD-QC02", "Operating Entity & Copyright (ACI SHWAPNO E-COMMERCE LIMITED, Copyright © 2026)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-QC02-20", "BD-QC02", "Operating Entity & Copyright (ACI SHWAPNO E-COMMERCE LIMITED, Copyright © 2026)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-QC02-20", "BD-QC02", "Operating Entity & Copyright (ACI SHWAPNO E-COMMERCE LIMITED, Copyright © 2026)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Shwapno", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),
]

csv_file = "results/information-gap-results-template.csv"

with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(f"Successfully appended {len(rows)} observations for BD-QC02 to {csv_file}")
