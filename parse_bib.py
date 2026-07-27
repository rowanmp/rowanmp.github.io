import re, os

os.makedirs('content/publications', exist_ok=True)

with open('citations.bib', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

entries = re.findall(r'@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}', content, re.DOTALL)

for entry_type, cite_key, fields in entries:
    title_match = re.search(r'\btitle\s*=\s*[\{\"](.*?)[^\\\}"]*[\}\"]', fields, re.DOTALL)
    author_match = re.search(r'\bauthor\s*=\s*[\{\"](.*?)[^\\\}"]*[\}\"]', fields, re.DOTALL)
    year_match = re.search(r'\byear\s*=\s*[\{\"]?(\d{4})[\}\"]?', fields)
    
    title = title_match.group(1).replace('\n', ' ').strip() if title_match else "Untitled"
    title = re.sub(r'[\{\}]', '', title)
    
    authors = author_match.group(1).replace('\n', ' ').strip() if author_match else "Rowan Martnishn"
    authors = re.sub(r'[\{\}]', '', authors)
    
    year = year_match.group(1) if year_match else "2026"
    
    # Clean filename
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', cite_key).lower()
    
    md_content = f\"\"\"---
title: \"{title}\"
date: {year}-01-01
draft: false
---

### {title}
**Authors:** {authors}  
**Year:** {year}  
**BibTeX Key:** {cite_key}
\"\"\"
    
    with open(f'content/publications/{safe_name}.md', 'w', encoding='utf-8') as out:
        out.write(md_content)

print(f"Successfully parsed {len(entries)} publications into content/publications/!")
