import re
from bs4 import BeautifulSoup

def html_to_jsx(html):
    html = html.replace('class=', 'className=')
    html = html.replace('onclick=', 'onClick=')
    html = html.replace('onchange=', 'onChange=')
    html = html.replace('oninput=', 'onInput=')
    html = html.replace('for=', 'htmlFor=')
    html = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', html)
    # Fix inline styles (very basic)
    html = re.sub(r'style="height:\s*([^;]+);"', r'style={{ height: "\1" }}', html)
    # self-closing tags
    html = html.replace('<hr>', '<hr/>').replace('<br>', '<br/>').replace('<img>', '<img/>')
    html = re.sub(r'<input([^>]*[^/])>', r'<input\1/>', html)
    return html

with open('scholarmap_platformasi.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

tabs = {
    'Baholash': soup.find(id='tab-baholash'),
    'Bazasi': soup.find(id='tab-bazasi'),
    'Qidirish': soup.find(id='tab-qidirish'),
    'Profil': soup.find(id='tab-profil'),
    'Tarjima': soup.find(id='tab-tarjima'),
    'Moliya': soup.find(id='tab-moliya'),
}

for name, tag in tabs.items():
    if not tag: continue
    jsx = html_to_jsx(str(tag))
    with open(f'scholarmap-frontend/src/{name}.tsx', 'w', encoding='utf-8') as f:
        f.write(f'export default function {name}() {{\n  return (\n    <>\n      {jsx}\n    </>\n  );\n}}\n')

sidebar = soup.find('aside')
if sidebar:
    with open('scholarmap-frontend/src/Sidebar.tsx', 'w', encoding='utf-8') as f:
        f.write(f'export default function Sidebar() {{\n  return (\n    <>\n      {html_to_jsx(str(sidebar))}\n    </>\n  );\n}}\n')

header = soup.find('header')
if header:
    with open('scholarmap-frontend/src/Header.tsx', 'w', encoding='utf-8') as f:
        f.write(f'export default function Header() {{\n  return (\n    <>\n      {html_to_jsx(str(header))}\n    </>\n  );\n}}\n')

print("Components extracted successfully.")
