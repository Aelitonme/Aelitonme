#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timezone
from html import escape

USERNAME = os.getenv("GITHUB_USERNAME", "Aelitonme")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT = os.getenv("OUTPUT_FILE", "dist/github-analytics.svg")
API = "https://api.github.com"

def get(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-analytics",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def repos():
    out, page = [], 1
    while True:
        batch = get(f"/users/{USERNAME}/repos?per_page=100&page={page}&type=owner")
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [r for r in out if not r.get("fork") and not r.get("archived")]

def stats(rs):
    langs = {}
    for r in rs:
        try:
            data = get(f"/repos/{USERNAME}/{r['name']}/languages")
        except Exception as e:
            print("WARN", r["name"], e)
            continue
        for name, size in data.items():
            langs[name] = langs.get(name, 0) + int(size)

    total = sum(langs.values())
    ranked = sorted(langs.items(), key=lambda x: x[1], reverse=True)
    percentages = [(name, (size / total * 100 if total else 0)) for name, size in ranked]

    return {
        "repos": len(rs),
        "stars": sum(r.get("stargazers_count", 0) for r in rs),
        "forks": sum(r.get("forks_count", 0) for r in rs),
        "total": total,
        "langs": percentages[:8],
    }

def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return str(n)

def svg(s):
    colors = ["#B57BFF","#9745F5","#7A3DB8","#663399","#5B2C6F","#4B247A","#351A57","#2A1745"]
    rows = []
    start_y, row_h = 230, 34

    if not s["langs"]:
        rows.append(f'<text x="52" y="{start_y}" class="muted">Nenhuma linguagem detectada ainda.</text>')
    else:
        for i, (lang, pct) in enumerate(s["langs"]):
            y = start_y + i * row_h
            w = max(2, min(100, pct)) * 4.6
            c = colors[i % len(colors)]
            rows.append(f"""
            <text x="52" y="{y+13}" class="lang">{escape(lang)}</text>
            <rect x="205" y="{y}" rx="7" width="460" height="14" fill="#1B1F2A"/>
            <rect x="205" y="{y}" rx="7" width="{w:.1f}" height="14" fill="{c}">
              <animate attributeName="width" from="0" to="{w:.1f}" dur="1.2s" fill="freeze"/>
            </rect>
            <text x="690" y="{y+13}" class="pct">{pct:.1f}%</text>
            """)

    h = 285 + max(5, len(s["langs"])) * row_h
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="{h}" viewBox="0 0 820 {h}">
    <defs>
      <linearGradient id="bg"><stop stop-color="#0D1117"/><stop offset="1" stop-color="#161022"/></linearGradient>
      <linearGradient id="accent"><stop stop-color="#7A3DB8"/><stop offset=".5" stop-color="#9745F5"/><stop offset="1" stop-color="#B57BFF"/></linearGradient>
    </defs>
    <style>
      .title{{font:700 24px Segoe UI,Arial;fill:#fff;letter-spacing:1px}}
      .sub,.label,.muted{{font:500 12px Segoe UI,Arial;fill:#8B949E}}
      .num{{font:700 26px Segoe UI,Arial;fill:#B57BFF}}
      .section{{font:700 15px Segoe UI,Arial;fill:#fff}}
      .lang{{font:600 13px Segoe UI,Arial;fill:#fff}}
      .pct{{font:700 13px Segoe UI,Arial;fill:#B57BFF}}
    </style>
    <rect x="1" y="1" width="818" height="{h-2}" rx="18" fill="url(#bg)" stroke="#2A1745" stroke-width="2"/>
    <rect x="28" y="28" width="6" height="58" rx="3" fill="url(#accent)"/>
    <text x="52" y="55" class="title">{USERNAME.upper()} // GITHUB ANALYTICS</text>
    <text x="52" y="78" class="sub">Cybersecurity • Network Security • Python</text>
    <line x1="52" y1="105" x2="768" y2="105" stroke="#252B36"/>
    <text x="62" y="137" class="label">REPOSITÓRIOS</text><text x="62" y="170" class="num">{s['repos']}</text>
    <text x="285" y="137" class="label">STARS</text><text x="285" y="170" class="num">{s['stars']}</text>
    <text x="480" y="137" class="label">FORKS</text><text x="480" y="170" class="num">{s['forks']}</text>
    <text x="650" y="137" class="label">CÓDIGO</text><text x="650" y="170" class="num">{fmt(s['total'])}</text>
    <text x="52" y="205" class="section">LANGUAGE DISTRIBUTION</text>
    {''.join(rows)}
    <text x="52" y="{h-28}" class="sub">Atualizado automaticamente em {updated}</text>
    <circle cx="760" cy="{h-32}" r="5" fill="#9745F5">
      <animate attributeName="opacity" values=".35;1;.35" dur="2s" repeatCount="indefinite"/>
    </circle>
    </svg>"""

def main():
    os.makedirs(os.path.dirname(OUTPUT) or ".", exist_ok=True)
    s = stats(repos())
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg(s))
    print("Gerado:", OUTPUT)
    print("Repos:", s["repos"], "Stars:", s["stars"], "Forks:", s["forks"])
    for name, pct in s["langs"]:
        print(f"{name}: {pct:.1f}%")

if __name__ == "__main__":
    main()
