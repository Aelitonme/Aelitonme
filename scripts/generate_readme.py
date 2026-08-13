#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote_plus
import yaml

data = yaml.safe_load(Path("profile-data.yml").read_text(encoding="utf-8"))
p = data["profile"]
username = p.get("username", "Aelitonme")
name = p.get("name", username)
role = p.get("role", "Cybersecurity Student")
headline = p.get("headline", "Cybersecurity • Network Security • Python")
bio = p.get("bio", "")
status = p.get("status", "Learning & Building")
focus = data.get("focus", [])
settings = data.get("settings", {})
certs = data.get("certifications", [])
platforms = data.get("platforms", [])
methodology = data.get("methodology", [])
objective = data.get("career", {}).get("objective", "")

typing = ";".join(quote_plus(x) for x in ["$ whoami", role, *focus[:4], status])
lines = []

lines += [
"<!-- AUTO-GENERATED FROM profile-data.yml -->",
"",
'<div align="center">',
f'<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=190&color=gradient&customColorList=6,12,20&text={quote_plus(name)}&fontColor=ffffff&fontSize=42&fontAlignY=35&desc={quote_plus(headline)}&descAlignY=58&animation=fadeIn"/>',
"",
f'<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=2800&pause=800&color=9745F5&center=true&vCenter=true&repeat=true&width=760&height=55&lines={typing}" alt="Typing animation"/>',
"",
f'<img src="https://komarev.com/ghpvc/?username={username}&label=PROFILE+VIEWS&color=6f42c1&style=for-the-badge" alt="Profile views"/>',
"",
f"### 🛡️ {headline}",
"</div>",
"",
"---",
"",
"## 🛡️ `whoami`",
"",
"```bash",
f"┌──({username.lower()}㉿cybersec)-[~]",
"└─$ whoami",
"",
name,
role,
headline,
f"Status: {status}",
"```",
"",
bio,
"",
"### 🎯 Current Focus",
"",
]

for item in focus:
    lines.append(f"- `{item}`")

if methodology:
    lines += ["", "### 🔁 Método de aprendizado", "", " → ".join(f"**{x}**" for x in methodology)]

if settings.get("show_analytics", True):
    lines += [
        "", "---", "", '<div align="center">', "", "## 📊 GitHub Analytics", "",
        f'<img src="https://raw.githubusercontent.com/{username}/{username}/gh-pages/github-analytics.svg" alt="GitHub Analytics" width="820"/>',
        "", "</div>", "",
        "> Linguagens, porcentagens, repositórios, stars e forks são atualizados automaticamente."
    ]

if settings.get("show_knowledge", True):
    lines += [
        "", "---", "", '<div align="center">', "", "## 🧠 Cybersecurity Knowledge", "",
        f'<img src="https://raw.githubusercontent.com/{username}/{username}/gh-pages/knowledge.svg" alt="Knowledge Dashboard" width="820"/>',
        "", "</div>", "",
        "> Os status de aprendizado vêm diretamente do `profile-data.yml`."
    ]

if settings.get("show_projects", True):
    lines += [
        "", "---", "", '<div align="center">', "", "## 🚀 Active Projects", "",
        f'<img src="https://raw.githubusercontent.com/{username}/{username}/gh-pages/projects.svg" alt="Projects Dashboard" width="820"/>',
        "", "</div>", "",
        "> Projetos e linguagens são detectados automaticamente nos repositórios públicos."
    ]

if settings.get("show_certifications", True) and certs:
    lines += ["", "---", "", "## 🎓 Certifications", ""]
    for cert in certs:
        label = cert.get("status", "").replace("_", " ").title()
        lines.append(f"- **{cert.get('name','Certification')}** — {cert.get('issuer','')} · `{label}`")

if settings.get("show_platforms", True) and platforms:
    badge_map = {
        "TryHackMe": "https://img.shields.io/badge/TryHackMe-212C42?style=for-the-badge&logo=tryhackme&logoColor=white",
        "Hack The Box": "https://img.shields.io/badge/Hack_The_Box-9FEF00?style=for-the-badge&logo=hackthebox&logoColor=black",
        "GitHub": "https://img.shields.io/badge/GitHub-111111?style=for-the-badge&logo=github&logoColor=white",
    }
    lines += ["", "---", "", '<div align="center">', "", "## 🧪 Platforms", ""]
    for platform in platforms:
        url = badge_map.get(platform)
        if url:
            lines.append(f'<img src="{url}" alt="{platform}"/>')
    lines += ["", "</div>"]

if settings.get("show_streak", True):
    lines += [
        "", "---", "", '<div align="center">', "", "## 🔥 Contribution Streak", "",
        f'<img src="https://streak-stats.demolab.com?user={username}&theme=tokyonight&hide_border=true&background=0D1117&ring=9745F5&fire=B57BFF&currStreakLabel=9745F5&sideLabels=FFFFFF&dates=8B949E" alt="GitHub Streak"/>',
        "", "</div>"
    ]

if objective:
    lines += ["", "---", "", "## 🎯 Objetivo profissional", "", objective]

if settings.get("show_snake", True):
    lines += [
        "", "---", "", '<div align="center">', "", "## 🐍 Contribution Snake", "",
        "<picture>",
        f'  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{username}/{username}/gh-pages/github-contribution-grid-snake-dark.svg">',
        f'  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{username}/{username}/gh-pages/github-contribution-grid-snake.svg">',
        f'  <img alt="GitHub contribution snake animation" src="https://raw.githubusercontent.com/{username}/{username}/gh-pages/github-contribution-grid-snake.svg">',
        "</picture>",
        "", "</div>"
    ]

lines += [
    "", "---", "", '<div align="center">', "", "## 💜 Cybersecurity Journey", "",
    '<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=2200&pause=650&color=B57BFF&center=true&vCenter=true&repeat=true&width=650&lines=%5B%2B%5D+Learn;%5B%2B%5D+Practice;%5B%2B%5D+Document;%5B%2B%5D+Build;%5B%2B%5D+Repeat" alt="Journey animation"/>',
    "", f"### `{headline}`", "",
    '<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=gradient&customColorList=6,12,20"/>',
    "", "</div>", ""
]

Path("Readme.md").write_text("\n".join(lines), encoding="utf-8")
print("Readme.md regenerated from profile-data.yml")
