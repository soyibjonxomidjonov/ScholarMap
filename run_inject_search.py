import os
from inject_search import search_jsx

with open('scholarmap-frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_ts = f.read()

start_idx = app_ts.find("case 'eligibility':")

if start_idx != -1:
    app_ts = app_ts[:start_idx] + "case 'search':\n        return (\n" + search_jsx + "        );\n\n      " + app_ts[start_idx:]
    with open('scholarmap-frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_ts)
    print("Injected search case!")
else:
    print("Could not find eligibility tag")
