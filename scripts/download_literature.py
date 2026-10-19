import os
import json
import time
import urllib.request
import urllib.error

PAPERS = [
    {
        "id": "2401.13649",
        "slug": "visualwebarena",
        "title": "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks",
        "year": "2024",
        "authors": ["Jing Yu Koh", "Robert Lo", "Lawrence Jang", "Vikram Duvvur", "Po-Yu Huang", "Graham Neubig", "Shuyan Zhou", "Daniel Fried"]
    },
    {
        "id": "2506.10953",
        "slug": "build-web-for-agents",
        "title": "Build the web for agents, not agents for the web",
        "year": "2025",
        "authors": ["Xing Han Lu", "Gaurav Kamath", "Marius Mosbach", "Siva Reddy"]
    },
    {
        "id": "2401.13919",
        "slug": "webvoyager",
        "title": "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models",
        "year": "2024",
        "authors": ["Hongliang He", "Wenlin Yao", "Kaixin Ma", "Wenhao Yu", "Yong Dai", "Hongming Zhang", "Zhenzhong Lan", "Dong Yu"]
    },
    {
        "id": "2510.01524",
        "slug": "walt-web-agents-learn-tools",
        "title": "WALT: Web Agents that Learn Tools",
        "year": "2025",
        "authors": ["Viraj Prabhu", "Yutong Dai", "Matthew Fernandez", "Jing Gu", "Krithika Ramakrishnan", "Yanqi Luo", "Silvio Savarese", "Caiming Xiong", "Junnan Li", "Zeyuan Chen", "Ran Xu"]
    },
    {
        "id": "2508.04412",
        "slug": "beyond-pixels-dom-downsampling",
        "title": "Beyond Pixels: Exploring DOM Downsampling for LLM-Based Web Agents",
        "year": "2025",
        "authors": ["Thassilo M. Schiepanski", "Nicholas Piel"]
    },
    {
        "id": "2604.08516",
        "slug": "molmoweb",
        "title": "MolmoWeb: Open Visual Web Agent and Open Data for the Open Web",
        "year": "2026",
        "authors": ["Tanmay Gupta", "Piper Wolters", "Zixian Ma", "Peter Sushko", "Rock Yuren Pang", "Ali Farhadi", "Ranjay Krishna"]
    },
    {
        "id": "2307.13854",
        "slug": "webarena",
        "title": "WebArena: A Realistic Web Environment for Building Autonomous Agents",
        "year": "2023",
        "authors": ["Shuyan Zhou", "Frank F. Xu", "Hao Zhu", "Xuhui Zhou", "Robert Lo", "Daniel Fried", "Uri Alon", "Graham Neubig"]
    }
]

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "papers"))

def fetch_paper_data(paper_info):
    slug = paper_info["slug"]
    paper_id = paper_info["id"]
    target_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(target_dir, exist_ok=True)
    
    pdf_path = os.path.join(target_dir, f"{paper_id}.pdf")
    meta_path = os.path.join(target_dir, "metadata.json")
    text_path = os.path.join(target_dir, "paper.txt")
    
    print(f"[{slug}] Processing {paper_id}: {paper_info['title']}...")
    
    # 1. Download PDF if not present
    if not os.path.exists(pdf_path):
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        print(f"  Downloading PDF from {pdf_url}...")
        req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(pdf_path, "wb") as out:
                    out.write(resp.read())
            print(f"  Saved PDF to {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        except Exception as e:
            print(f"  Failed to download PDF: {e}")
    else:
        print(f"  PDF already exists: {pdf_path}")
        
    # 2. Fetch HTML / text representation from arXiv HTML endpoint if available
    if not os.path.exists(text_path):
        html_url = f"https://arxiv.org/html/{paper_id}"
        print(f"  Fetching text / HTML from {html_url}...")
        req = urllib.request.Request(html_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                with open(text_path, "w", encoding="utf-8") as out:
                    out.write(content)
            print(f"  Saved HTML text to {text_path} ({len(content)} chars)")
        except Exception as e:
            print(f"  HTML endpoint unavailable ({e}); extracting abstract...")
            # Fallback to abstract endpoint
            abs_url = f"https://arxiv.org/abs/{paper_id}"
            req_abs = urllib.request.Request(abs_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            try:
                with urllib.request.urlopen(req_abs, timeout=20) as resp:
                    content = resp.read().decode("utf-8", errors="ignore")
                    with open(text_path, "w", encoding="utf-8") as out:
                        out.write(content)
                print(f"  Saved abstract page to {text_path}")
            except Exception as e2:
                print(f"  Failed abstract fetch: {e2}")
    else:
        print(f"  Text already exists: {text_path}")

    # 3. Save Metadata
    with open(meta_path, "w", encoding="utf-8") as out:
        json.dump(paper_info, out, indent=2)
    print(f"  Metadata saved: {meta_path}")

def main():
    print(f"Target Papers Directory: {BASE_DIR}")
    for p in PAPERS:
        fetch_paper_data(p)
        time.sleep(2)  # Respectful delay between requests
    print("\nAll literature downloaded successfully.")

if __name__ == "__main__":
    main()
