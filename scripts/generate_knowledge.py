from pathlib import Path
from html import escape
import re

data = {}
category = None
inside_learning = False

for raw in Path("profile-data.yml").read_text(encoding="utf-8").splitlines():
    if raw == "learning:":
        inside_learning = True
        continue

    if inside_learning and raw and not raw.startswith(" "):
        break

    if not inside_learning:
        continue

    category_match = re.match(r"^  ([^:]+):\s*$", raw)
    if category_match:
        category = category_match.group(1)
        data[category] = []
        continue

    item_match = re.match(
        r"^    ([^:]+):\s*(learned|practicing|studying|next)\s*$",
        raw
    )

    if item_match and category:
        data[category].append(
            (item_match.group(1), item_match.group(2))
        )

labels = {
    "learned": ("✓", "LEARNED", "#B57BFF"),
    "practicing": ("◉", "PRACTICING", "#9745F5"),
    "studying": ("●", "STUDYING", "#7A3DB8"),
    "next": ("→", "NEXT", "#8B949E"),
}

y = 135
body = []

for category, items in data.items():
    body.append(
        f'<text x="52" y="{y}" class="cat">{escape(category.upper())}</text>'
    )
    y += 28

    for name, status in items:
        icon, label, color = labels[status]

        body.append(
            f'<text x="65" y="{y}" class="item">{escape(name)}</text>'
            f'<text x="545" y="{y}" class="status" fill="{color}">'
            f'{icon} {label}</text>'
        )

        y += 27

    y += 18

height = y + 45

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="{height}" viewBox="0 0 820 {height}">
<style>
.title{{font:700 23px Arial;fill:white}}
.sub{{font:12px Arial;fill:#8B949E}}
.cat{{font:700 14px Arial;fill:#B57BFF}}
.item{{font:13px Arial;fill:#F0F3F6}}
.status{{font:700 11px Arial}}
</style>

<rect width="820" height="{height}" rx="18"
      fill="#0D1117" stroke="#2A1745" stroke-width="2"/>

<rect x="28" y="28" width="6" height="58"
      rx="3" fill="#9745F5"/>

<text x="52" y="55" class="title">CYBERSECURITY KNOWLEDGE</text>

<text x="52" y="78" class="sub">
Learning dashboard • generated from profile-data.yml
</text>

<line x1="52" y1="104" x2="768" y2="104"
      stroke="#252B36"/>

{''.join(body)}

<text x="52" y="{height-26}" class="sub">
✓ learned   ◉ practicing   ● studying   → next
</text>

<circle cx="760" cy="{height-30}" r="5" fill="#9745F5">
  <animate
    attributeName="opacity"
    values=".3;1;.3"
    dur="2s"
    repeatCount="indefinite"
  />
</circle>

</svg>"""

Path("dist").mkdir(exist_ok=True)
Path("dist/knowledge.svg").write_text(svg, encoding="utf-8")

print("Knowledge dashboard gerado com sucesso.")
for category, items in data.items():
    print(f"{category}: {len(items)} itens")
