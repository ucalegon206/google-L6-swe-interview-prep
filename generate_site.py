import os
import re
import glob
import json
from pathlib import Path

# Configuration
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
STUDY_GUIDE_FILE = os.path.join(REPO_DIR, "study_guide_by_pattern.md")
SYSTEM_DESIGN_FILE = os.path.join(REPO_DIR, "system_design_protocol.md")

# Manual Mapping for Study Guide Name -> Problem Name in File
NAME_MAPPING = {
    "minwindowsubstring": "minimumwindowsubstring",
    "slidingwindowmax": "slidingwindowmaximum",
    "median2itemssortedarrays": "medianoftwosortedarrays", # Potential mismatch
    "median2sortedarrays": "medianoftwosortedarrays",
    "countsmallerafterself": "countofsmallernumbersafterself",
    "removeinvalidparens": "removeinvalidparentheses",
    "searchautocomplete": "designsearchautocompletesystem",
    "mergekitemssortedlists": "mergeksortedlists", # Potential mismatch
}

def normalize(text):
    """Normalize text for fuzzy matching (lowercase, alphanumeric only)."""
    clean = re.sub(r'[^a-z0-9]', '', text.lower())
    return NAME_MAPPING.get(clean, clean)

def parse_solutions():
    """Parse all _*.py files to extract problem metadata and content."""
    solutions = {}
    
    # Get all solution files (start with underscore and digit)
    files = glob.glob(os.path.join(REPO_DIR, "_*.py"))
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Problem Name
        match = re.search(r'PROBLEM:\s*(.+)', content)
        if match:
            raw_name = match.group(1).strip()
            key = normalize(raw_name)
            
            # Extract Docstring (Explanation) vs Code
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            explanation = ""
            if docstring_match:
                explanation = docstring_match.group(1).strip()
            
            solutions[key] = {
                'raw_name': raw_name,
                'filename': filename,
                'explanation': explanation,
                'code': content
            }
    return solutions

def parse_study_guide():
    """Parse the markdown guide to get the structure and analogies."""
    with open(STUDY_GUIDE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    structure = []
    current_pattern = None
    
    for line in lines:
        line = line.strip()
        
        # Pattern Header
        if line.startswith("## ") and re.match(r'## \d+\.', line):
            if current_pattern:
                structure.append(current_pattern)
            
            current_pattern = {
                'name': line.replace("## ", ""),
                'analogy': "",
                'mnemonic': "",
                'problems': []
            }
            continue
            
        # Metadata (Analogy / Mnemonic)
        if "**Analogy:**" in line:
            if current_pattern:
                current_pattern['analogy'] = line.split("**Analogy:**")[1].strip()
        if "**Mnemonic:**" in line:
            if current_pattern:
                current_pattern['mnemonic'] = line.split("**Mnemonic:**")[1].strip()
                
        # Problem Row
        if line.startswith("|") and "**" in line:
            match = re.search(r'\*\*(.*?)\*\*', line)
            if match and current_pattern:
                prob_name = match.group(1)
                current_pattern['problems'].append(prob_name)
                
    if current_pattern:
        structure.append(current_pattern)
        
    return structure

def parse_system_design():
    """Read the system design protocol markdown."""
    if not os.path.exists(SYSTEM_DESIGN_FILE):
        return "System Design Protocol not found."
    with open(SYSTEM_DESIGN_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def generate_html(structure, solutions, system_design_content):
    """Generate the single-page HTML."""
    
    sidebar_html = """
    <div class="category">
        <h3>System Design</h3>
        <div class="problem-list" style="display:block">
            <a href="#system-design" class="nav-link" onclick="activateLink(this)">The Anti-Freeze Protocol</a>
        </div>
    </div>
    """
    
    content_html = f"""
    <div id="system-design" class="pattern-section">
        <div class="problem-block" style="padding: 30px;">
            <div class="explanation-text"><pre>{system_design_content}</pre></div>
        </div>
    </div>
    """
    
    for pattern in structure:
        p_id = normalize(pattern['name'])
        
        # Sidebar Category
        sidebar_html += f"""
        <div class="category">
            <h3 onclick="toggleCategory('{p_id}')">{pattern['name']}</h3>
            <div id="cat-{p_id}" class="problem-list">
        """
        
        # Main Pattern Header
        content_html += f"""
        <div id="pattern-{p_id}" class="pattern-section">
            <h1 class="gradient-text">{pattern['name']}</h1>
            <div class="card mnemonic-card">
                <p><strong>Analogy:</strong> {pattern['analogy']}</p>
                <p class="highlight"><strong>Mnemonic:</strong> {pattern['mnemonic']}</p>
            </div>
        """
        
        for prob_name in pattern['problems']:
            key = normalize(prob_name)
            sol = solutions.get(key)
            
            if not sol:
                print(f"WARNING: Could not find solution for '{prob_name}' (key: {key})")
                continue
                
            prob_id = normalize(prob_name)
            
            # Sidebar Link
            sidebar_html += f"""
                <a href="#prob-{prob_id}" class="nav-link" onclick="activateLink(this)">{sol['raw_name']}</a>
            """
            
            # Problem Content
            content_html += f"""
            <div id="prob-{prob_id}" class="problem-block">
                <div class="problem-header">
                    <h2>{sol['raw_name']}</h2>
                    <span class="badge">{sol['filename']}</span>
                </div>
                
                <div class="tabs">
                    <button class="tab-btn active" onclick="openTab(event, 'expl-{prob_id}')">Explanation</button>
                    <button class="tab-btn" onclick="openTab(event, 'code-{prob_id}')">Code</button>
                    <a href="https://www.google.com/search?q={sol['raw_name']}+leetcode" target="_blank" class="ext-link">LeetCode ↗</a>
                </div>
                
                <div id="expl-{prob_id}" class="tab-content active">
                    <div class="explanation-text">
                        <pre>{sol['explanation']}</pre>
                    </div>
                </div>
                
                <div id="code-{prob_id}" class="tab-content">
                    <pre><code class="language-python">{sol['code']}</code></pre>
                </div>
            </div>
            """
            
        # Close Sidebar Category
        sidebar_html += "</div></div>"
        
        # Close Pattern Section
        content_html += "</div>"
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>L6 Anti-Freeze Playbook</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <style>
        :root {{
            --bg-color: #0d1117;
            --sidebar-bg: #161b22;
            --text-color: #c9d1d9;
            --accent-color: #58a6ff;
            --border-color: #30363d;
            --card-bg: #21262d;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        
        .sidebar {{
            width: 320px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }}
        
        .sidebar-header {{
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .sidebar-header h2 {{
            margin: 0;
            font-size: 1.2rem;
            color: var(--accent-color);
        }}
        
        .search-box {{
            padding: 15px;
        }}
        
        .search-input {{
            width: 90%;
            padding: 10px;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            border-radius: 6px;
        }}
        
        .nav-content {{
            overflow-y: auto;
            flex: 1;
            padding: 10px;
        }}
        
        .category h3 {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #8b949e;
            cursor: pointer;
            padding: 10px;
            margin: 5px 0;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
        }}
        
        .category h3:hover {{
            background-color: var(--card-bg);
            color: var(--text-color);
        }}
        
        .nav-link {{
            display: block;
            padding: 8px 10px 8px 25px;
            color: var(--text-color);
            text-decoration: none;
            font-size: 0.95rem;
            border-radius: 6px;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .nav-link:hover {{
            background-color: var(--card-bg);
        }}
        
        .nav-link.active {{
            background-color: #1f6feb22;
            color: var(--accent-color);
            border-left-color: var(--accent-color);
        }}
        
        .main {{
            flex: 1;
            overflow-y: auto;
            padding: 0;
            scroll-behavior: smooth;
        }}
        
        .content-container {{
            max-width: 960px;
            margin: 0 auto;
            padding: 40px;
        }}
        
        .pattern-section {{
            margin-bottom: 80px;
            scroll-margin-top: 20px;
        }}
        
        .gradient-text {{
            background: linear-gradient(90deg, #58a6ff, #a371f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }}
        
        .mnemonic-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-left: 5px solid #a371f7;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .mnemonic-card p {{
            margin: 5px 0;
            font-size: 1.1rem;
            line-height: 1.6;
        }}
        
        .highlight {{
            color: #a371f7;
            font-weight: bold;
            font-size: 1.2rem;
        }}
        
        .explanation-text pre {{
            white-space: pre-wrap;
            font-family: inherit;
            color: #c9d1d9;
            font-size: 1rem;
            line-height: 1.6;
            margin: 0;
        }}
        
        .problem-block {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 40px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}
        
        .problem-header {{
            padding: 15px 25px;
            background-color: #2b313a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .badge {{
            background: #21262d;
            border: 1px solid #30363d;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-family: monospace;
            color: #8b949e;
        }}
        
        .tabs {{
            display: flex;
            background: #161b22;
            padding: 0 20px;
            gap: 2px;
        }}
        
        .tab-btn {{
            background: none;
            border: none;
            color: #8b949e;
            padding: 15px 20px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            font-weight: 600;
        }}
        
        .tab-btn:hover {{
            color: var(--text-color);
        }}
        
        .tab-btn.active {{
            color: var(--accent-color);
            border-bottom-color: var(--accent-color);
        }}
        
        .ext-link {{
            margin-left: auto;
            color: var(--accent-color);
            text-decoration: none;
            font-size: 0.9rem;
            align-self: center;
            opacity: 0.8;
            padding-right: 20px;
        }}
        
        .ext-link:hover {{
            opacity: 1;
            text-decoration: underline;
        }}
        
        .tab-content {{
            display: none;
            padding: 30px;
            background: var(--card-bg);
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h2>🍧 Anti-Freeze Playbook</h2>
        </div>
        <div class="search-box">
            <input type="text" class="search-input" placeholder="Search..." onkeyup="filterNav()">
        </div>
        <div class="nav-content" id="sidebar-nav">
            {sidebar_html}
        </div>
    </div>
    
    <div class="main">
        <div class="content-container">
            {content_html}
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>
        function openTab(evt, tabId) {{
            let parent = evt.target.closest('.problem-block');
            let contents = parent.querySelectorAll('.tab-content');
            contents.forEach(c => c.style.display = 'none');
            let btns = parent.querySelectorAll('.tab-btn');
            btns.forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).style.display = 'block';
            evt.target.classList.add('active');
        }}
        
        function activateLink(el) {{
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            el.classList.add('active');
        }}
        
        function filterNav() {{
            let input = document.querySelector('.search-input').value.toLowerCase();
            let links = document.querySelectorAll('.nav-link');
            
            links.forEach(link => {{
                let text = link.innerText.toLowerCase();
                if (text.includes(input)) {{
                    link.style.display = "";
                }} else {{
                    link.style.display = "none";
                }}
            }});
        }}
        
        function toggleCategory(id) {{
            let el = document.getElementById('cat-' + id);
            if (el.style.display === 'none') {{
                el.style.display = 'block';
            }} else {{
                el.style.display = 'none';
            }}
        }}
    </script>
</body>
</html>
    """
    
    with open(os.path.join(REPO_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully generated index.html with {len(solutions)} problems and system design.")

if __name__ == "__main__":
    sols = parse_solutions()
    struct = parse_study_guide()
    sys_design = parse_system_design()
    generate_html(struct, sols, sys_design)
