#!/usr/bin/env python3
import json, os, urllib.request
from pathlib import Path
from html import escape
from datetime import datetime, timezone

USERNAME=os.getenv("GITHUB_USERNAME","Aelitonme")
TOKEN=os.getenv("GITHUB_TOKEN","")
API="https://api.github.com"
OUTPUT=Path("dist/projects.svg")
MAX_PROJECTS=4

def get(path):
    headers={"Accept":"application/vnd.github+json","User-Agent":f"{USERNAME}-profile-projects","X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN: headers["Authorization"]=f"Bearer {TOKEN}"
    req=urllib.request.Request(API+path,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def fetch_repos():
    repos=get(f"/users/{USERNAME}/repos?per_page=100&sort=updated&type=owner")
    out=[]
    for repo in repos:
        if repo.get("fork") or repo.get("archived"): continue
        if repo["name"].lower()==USERNAME.lower(): continue
        out.append(repo)
    return out[:MAX_PROJECTS]

def langs(name):
    try: data=get(f"/repos/{USERNAME}/{name}/languages")
    except Exception: return []
    return [k for k,_ in sorted(data.items(),key=lambda x:x[1],reverse=True)[:3]]

def fmt_date(value):
    try:
        return datetime.fromisoformat(value.replace("Z","+00:00")).strftime("%d/%m/%Y")
    except Exception:
        return "-"

def render(repos):
    width=820; card_h=150; gap=18; start_y=130
    height=start_y+max(1,len(repos))*(card_h+gap)+55
    rows=[]

    if not repos:
        rows.append('<text x="52" y="165" class="muted">Nenhum projeto público detectado ainda.</text>')
    else:
        for i,repo in enumerate(repos):
            y=start_y+i*(card_h+gap)
            l=langs(repo["name"])
            ltxt=" • ".join(l) if l else "Sem linguagem detectada"
            desc=repo.get("description") or "Projeto público no GitHub."
            if len(desc)>78: desc=desc[:75]+"..."
            updated=fmt_date(repo.get("pushed_at") or repo.get("updated_at") or "")
            rows.append(
                f'<rect x="42" y="{y}" width="736" height="{card_h}" rx="16" fill="#11161E" stroke="#2A1745"/>'
                f'<rect x="42" y="{y}" width="6" height="{card_h}" rx="3" fill="#9745F5"/>'
                f'<text x="68" y="{y+34}" class="name">{escape(repo["name"])}</text>'
                f'<text x="68" y="{y+58}" class="desc">{escape(desc)}</text>'
                f'<text x="68" y="{y+86}" class="langs">{escape(ltxt)}</text>'
                f'<text x="68" y="{y+116}" class="meta">Stars {repo.get("stargazers_count",0)}   Forks {repo.get("forks_count",0)}   Updated {updated}</text>'
                f'<text x="650" y="{y+116}" class="status">● ACTIVE</text>'
            )

    stamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body="".join(rows)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.title{{font:700 23px Arial;fill:#fff}}
.sub{{font:12px Arial;fill:#8B949E}}
.name{{font:700 17px Arial;fill:#B57BFF}}
.desc{{font:13px Arial;fill:#F0F3F6}}
.langs{{font:700 12px Arial;fill:#9745F5}}
.meta{{font:12px Arial;fill:#8B949E}}
.status{{font:700 11px Arial;fill:#B57BFF}}
.muted{{font:13px Arial;fill:#8B949E}}
</style>
<rect width="{width}" height="{height}" rx="18" fill="#0D1117" stroke="#2A1745" stroke-width="2"/>
<rect x="28" y="28" width="6" height="58" rx="3" fill="#9745F5"/>
<text x="52" y="55" class="title">ACTIVE PROJECTS</text>
<text x="52" y="78" class="sub">Automatically generated from public GitHub repositories</text>
<line x1="52" y1="104" x2="768" y2="104" stroke="#252B36"/>
{body}
<text x="52" y="{height-28}" class="sub">Updated automatically at {stamp}</text>
<circle cx="760" cy="{height-32}" r="5" fill="#9745F5"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></circle>
</svg>"""

repos=fetch_repos()
OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(render(repos),encoding="utf-8")
print("Projects dashboard generated.")
for repo in repos:
    print("-",repo["name"],":",", ".join(langs(repo["name"])) or "no language")
