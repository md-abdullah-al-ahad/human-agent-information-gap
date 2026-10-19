from html.parser import HTMLParser
import re

class SemanticExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        # Non-void tags whose contents should be ignored entirely
        self.skip_blocks = {'script', 'style', 'svg', 'noscript', 'head'}
        self.in_skip = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag in self.skip_blocks:
            self.in_skip += 1
            return
        if self.in_skip > 0:
            return

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag in ['p', 'div', 'section', 'article']:
            self.output.append("\n")
        elif tag == 'li':
            self.output.append("\n- ")
        elif tag == 'button':
            self.output.append(" [BUTTON: ")
        elif tag == 'a':
            href = attr_dict.get('href', '')
            self.output.append(f" [LINK({href}): ")
        elif tag == 'input':
            val = attr_dict.get('value', '') or attr_dict.get('placeholder', '')
            self.output.append(f" [INPUT: {val}] ")
        elif tag == 'img':
            src = attr_dict.get('src', '')
            alt = attr_dict.get('alt', '')
            title = attr_dict.get('title', '')
            self.output.append(f" [IMG alt='{alt}' title='{title}' src='{src}'] ")

    def handle_endtag(self, tag):
        if tag in self.skip_blocks:
            if self.in_skip > 0:
                self.in_skip -= 1
            return
        if self.in_skip > 0:
            return

        if tag in ['button', 'a']:
            self.output.append("] ")

    def handle_data(self, data):
        if self.in_skip > 0:
            return
        text = data.strip()
        if text:
            self.output.append(text + " ")

html_path = "data/stage-4/raw/bd-qc02-dom.html"
with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    html_content = f.read()

parser = SemanticExtractor()
parser.feed(html_content)
semantic_doc = "".join(parser.output)
# Clean multiple newlines and spaces
semantic_doc = re.sub(r'[ \t]+', ' ', semantic_doc)
semantic_doc = re.sub(r'\n\s*\n+', '\n\n', semantic_doc).strip()

print(f"Original size: {len(html_content):,} bytes")
print(f"Semantic Markdown size: {len(semantic_doc):,} bytes")
print(f"Token reduction: {100 - len(semantic_doc)/len(html_content)*100:.2f}%")
print("\n--- FIRST 2000 CHARACTERS OF SEMANTIC MARKDOWN ---")
print(semantic_doc[:2000])
