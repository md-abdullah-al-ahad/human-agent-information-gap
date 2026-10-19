import csv

rows = [
    # BD-FN02-01
    ("BD-FN02-01", "BD-FN02", "Nagad Logo Subtitle Tagline (ডাক বিভাগের ডিজিটাল লেনদেন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS (Extracted from logo asset)", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-01", "BD-FN02", "Nagad Logo Subtitle Tagline (ডাক বিভাগের ডিজিটাল লেনদেন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-01", "BD-FN02", "Nagad Logo Subtitle Tagline (ডাক বিভাগের ডিজিটাল লেনদেন)", "TEXT", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "No", "FAIL (Reported Not Found)", "Micro-Raster Legibility Barrier", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): FAIL (Illegible 5px raster in static screenshot)"),
    ("BD-FN02-01", "BD-FN02", "Nagad Logo Subtitle Tagline (ডাক বিভাগের ডিজিটাল লেনদেন)", "TEXT", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-02
    ("BD-FN02-02", "BD-FN02", "Active Language Selection (বাংলা active red pill)", "UI_STATE", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-02", "BD-FN02", "Active Language Selection (বাংলা active red pill)", "UI_STATE", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-02", "BD-FN02", "Active Language Selection (বাংলা active red pill)", "UI_STATE", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-02", "BD-FN02", "Active Language Selection (বাংলা active red pill)", "UI_STATE", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-03
    ("BD-FN02-03", "BD-FN02", "Main Nav Sixth Menu Link (নগদ ইসলামিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-03", "BD-FN02", "Main Nav Sixth Menu Link (নগদ ইসলামিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-03", "BD-FN02", "Main Nav Sixth Menu Link (নগদ ইসলামিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-03", "BD-FN02", "Main Nav Sixth Menu Link (নগদ ইসলামিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-04
    ("BD-FN02-04", "BD-FN02", "Popup Modal Headline (নগদ অ্যাপে নতুন Experience)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-04", "BD-FN02", "Popup Modal Headline (নগদ অ্যাপে নতুন Experience)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Analysis)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-04", "BD-FN02", "Popup Modal Headline (নগদ অ্যাপে নতুন Experience)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-04", "BD-FN02", "Popup Modal Headline (নগদ অ্যাপে নতুন Experience)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-05
    ("BD-FN02-05", "BD-FN02", "Popup Modal Central Slogan (সব হবে Nonstop)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-05", "BD-FN02", "Popup Modal Central Slogan (সব হবে Nonstop)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Analysis)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-05", "BD-FN02", "Popup Modal Central Slogan (সব হবে Nonstop)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-05", "BD-FN02", "Popup Modal Central Slogan (সব হবে Nonstop)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-06
    ("BD-FN02-06", "BD-FN02", "Popup Modal Brand Ambassador (Jamal Bhuyan / Tariq Kazi)", "VISUAL_ENTITY", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "No", "FAIL (Reported Not Found)", "Unlabeled Entity Visual Grounding Gap", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): FAIL (No alt text/name in markup)"),
    ("BD-FN02-06", "BD-FN02", "Popup Modal Brand Ambassador (Jamal Bhuyan / Tariq Kazi)", "VISUAL_ENTITY", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS (Tariq Kazi)", "None (Visual Entity Grounding)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-06", "BD-FN02", "Popup Modal Brand Ambassador (Jamal Bhuyan / Tariq Kazi)", "VISUAL_ENTITY", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "No", "FAIL (Reported Not Found)", "Unlabeled Entity Visual Grounding Gap", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): FAIL (No alt text/name in markup)"),
    ("BD-FN02-06", "BD-FN02", "Popup Modal Brand Ambassador (Jamal Bhuyan / Tariq Kazi)", "VISUAL_ENTITY", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS (Jamal Bhuyan)", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-07
    ("BD-FN02-07", "BD-FN02", "Popup Modal CTA Button (Let's go with right-arrow)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-07", "BD-FN02", "Popup Modal CTA Button (Let's go with right-arrow)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-07", "BD-FN02", "Popup Modal CTA Button (Let's go with right-arrow)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-07", "BD-FN02", "Popup Modal CTA Button (Let's go with right-arrow)", "BUTTON_UI", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-08
    ("BD-FN02-08", "BD-FN02", "Hero Slogan Behind Popup (লেনদেন যেখানে নগদ সেখানে)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-08", "BD-FN02", "Hero Slogan Behind Popup (লেনদেন যেখানে নগদ সেখানে)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-08", "BD-FN02", "Hero Slogan Behind Popup (লেনদেন যেখানে নগদ সেখানে)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-08", "BD-FN02", "Hero Slogan Behind Popup (লেনদেন যেখানে নগদ সেখানে)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-09
    ("BD-FN02-09", "BD-FN02", "Hero Shop Signboard Text (সর্বনিম্ন ক্যাশ আউট চার্জ)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-09", "BD-FN02", "Hero Shop Signboard Text (সর্বনিম্ন ক্যাশ আউট চার্জ)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-09", "BD-FN02", "Hero Shop Signboard Text (সর্বনিম্ন ক্যাশ আউট চার্জ)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-09", "BD-FN02", "Hero Shop Signboard Text (সর্বনিম্ন ক্যাশ আউট চার্জ)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (0% in DOM text)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-10
    ("BD-FN02-10", "BD-FN02", "Current Offers Section Heading (বর্তমান অফার)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-10", "BD-FN02", "Current Offers Section Heading (বর্তমান অফার)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-10", "BD-FN02", "Current Offers Section Heading (বর্তমান অফার)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-10", "BD-FN02", "Current Offers Section Heading (বর্তমান অফার)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-11
    ("BD-FN02-11", "BD-FN02", "Weekend Add Money Amount (৳৮,৮৮০ অ্যাড মানিতে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS (৳৪,৪৪০ / ৳৮,৮৮০)", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-11", "BD-FN02", "Weekend Add Money Amount (৳৮,৮৮০ অ্যাড মানিতে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-11", "BD-FN02", "Weekend Add Money Amount (৳৮,৮৮০ অ্যাড মানিতে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-11", "BD-FN02", "Weekend Add Money Amount (৳৮,৮৮০ অ্যাড মানিতে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-12
    ("BD-FN02-12", "BD-FN02", "Weekend Add Money Instant Bonus (৳৮০ ইনস্ট্যান্ট বোনাস)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS (৳৮০)", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-12", "BD-FN02", "Weekend Add Money Instant Bonus (৳৮০ ইনস্ট্যান্ট বোনাস)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-12", "BD-FN02", "Weekend Add Money Instant Bonus (৳৮০ ইনস্ট্যান্ট বোনাস)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-12", "BD-FN02", "Weekend Add Money Instant Bonus (৳৮০ ইনস্ট্যান্ট বোনাস)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-13
    ("BD-FN02-13", "BD-FN02", "DeeptoPlay Cashback (২০% ক্যাশব্যাক নগদ পেমেন্টে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS (২০%)", "None (Visual Crop)", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-13", "BD-FN02", "DeeptoPlay Cashback (২০% ক্যাশব্যাক নগদ পেমেন্টে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None (Visual Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-13", "BD-FN02", "DeeptoPlay Cashback (২০% ক্যাশব্যাক নগদ পেমেন্টে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None (Compensatory Cropping)", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-13", "BD-FN02", "DeeptoPlay Cashback (২০% ক্যাশব্যাক নগদ পেমেন্টে)", "IN_IMAGE_GRAPHIC", "Yes (Visual screenshot)", "No (Trapped CSS background)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None (Static Asset Crop)", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-14
    ("BD-FN02-14", "BD-FN02", "Account Opening Heading (নগদ একাউন্ট খুলুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-14", "BD-FN02", "Account Opening Heading (নগদ একাউন্ট খুলুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-14", "BD-FN02", "Account Opening Heading (নগদ একাউন্ট খুলুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-14", "BD-FN02", "Account Opening Heading (নগদ একাউন্ট খুলুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-15
    ("BD-FN02-15", "BD-FN02", "Account Opening Subheading (আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-15", "BD-FN02", "Account Opening Subheading (আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-15", "BD-FN02", "Account Opening Subheading (আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-15", "BD-FN02", "Account Opening Subheading (আপনার নগদ একাউন্ট তৈরি করার ৩ টি সহজ ধাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-16
    ("BD-FN02-16", "BD-FN02", "Account Opening Step 1 (এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-16", "BD-FN02", "Account Opening Step 1 (এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-16", "BD-FN02", "Account Opening Step 1 (এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-16", "BD-FN02", "Account Opening Step 1 (এন আই ডি স্ক্যান করে প্রয়োজনীয় তথ্য দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-17
    ("BD-FN02-17", "BD-FN02", "Account Opening Step 2 (সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-17", "BD-FN02", "Account Opening Step 2 (সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-17", "BD-FN02", "Account Opening Step 2 (সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-17", "BD-FN02", "Account Opening Step 2 (সেলফি তুলুন ও নির্দিষ্ট জায়গায় ডিজিটাল স্বাক্ষর দিন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-18
    ("BD-FN02-18", "BD-FN02", "Account Opening Step 3 (৪ ডিজিটের পিন সেট করুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-18", "BD-FN02", "Account Opening Step 3 (৪ ডিজিটের পিন সেট করুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-18", "BD-FN02", "Account Opening Step 3 (৪ ডিজিটের পিন সেট করুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-18", "BD-FN02", "Account Opening Step 3 (৪ ডিজিটের পিন সেট করুন)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-19
    ("BD-FN02-19", "BD-FN02", "Postal DFS Milestone (২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-19", "BD-FN02", "Postal DFS Milestone (২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-19", "BD-FN02", "Postal DFS Milestone (২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-19", "BD-FN02", "Postal DFS Milestone (২০১৯ সালের ২৬ মার্চ and ৯ কোটির অধিক)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),

    # BD-FN02-20
    ("BD-FN02-20", "BD-FN02", "Copyright & App Download CTA (© 2026 Nagad All rights reserved, ডাউনলোড অ্যাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "OpenCode/Qwen3.8-27B (With Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (With Playwright): PASS"),
    ("BD-FN02-20", "BD-FN02", "Copyright & App Download CTA (© 2026 Nagad All rights reserved, ডাউনলোড অ্যাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Playwright)", "Antigravity/Gemini 3.8 Flash (With Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (With Playwright): PASS"),
    ("BD-FN02-20", "BD-FN02", "Copyright & App Download CTA (© 2026 Nagad All rights reserved, ডাউনলোড অ্যাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "OpenCode/Qwen3.8-27B (Without Playwright)", "Yes", "PASS", "None", "Nagad", "OpenCode/Qwen3.8-27B (Without Playwright): PASS"),
    ("BD-FN02-20", "BD-FN02", "Copyright & App Download CTA (© 2026 Nagad All rights reserved, ডাউনলোড অ্যাপ)", "TEXT", "Yes (Visual screenshot)", "Yes (Static DOM)", "Antigravity/Gemini 3.8 Flash (Without Playwright)", "Yes", "PASS", "None", "Nagad", "Antigravity/Gemini 3.8 Flash (Without Playwright): PASS"),
]

# Read all existing lines except BD-FN02
with open("results/information-gap-results-template.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    existing_rows = [row for row in reader if len(row) > 1 and row[1] != "BD-FN02"]

with open("results/information-gap-results-template.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for r in existing_rows:
        writer.writerow(r)
    for r in rows:
        writer.writerow(r)

print(f"Updated Nagad in results CSV: {len(existing_rows)-1} other rows + {len(rows)} Nagad rows = {len(existing_rows)-1+len(rows)} total observations.")
