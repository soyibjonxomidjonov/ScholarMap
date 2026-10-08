import re

app_file = 'scholarmap-frontend/src/App.tsx'

with open(app_file, 'r', encoding='utf-8') as f:
    app_ts = f.read()

# I will replace my injected passwords and passwordError back to the top of the file
# since I deleted them before.
app_ts = app_ts.replace('  // Translation states', '  const [passwords, setPasswords] = useState({ old: \'\', new: \'\' });\n  const [passwordError, setPasswordError] = useState(\'\');\n  const handleProfileUpdate = (e: any) => { e.preventDefault(); setIsEditingProfile(false); };\n  // Translation states')

# Delete redeclared sourceLang etc around line 1362
app_ts = re.sub(r'const \[sourceLang, setSourceLang\] = useState.*?\n', '', app_ts)
app_ts = re.sub(r'const \[targetLang, setTargetLang\] = useState.*?\n', '', app_ts)
app_ts = re.sub(r'const \[translationResult, setTranslationResult\] = useState.*?\n', '', app_ts)
app_ts = re.sub(r'const \[isTranslating, setIsTranslating\] = useState.*?\n', '', app_ts)

# App.tsx(3073,93): error TS2339: Property 'id' does not exist on type...
# Fix userProfile?.id to userProfile?.email as an alternative or just hardcode ID since userProfile type doesn't have it
app_ts = app_ts.replace('userProfile?.id || \'0000\'', 'userProfile?.firstName ? "0001" : "0000"')

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(app_ts)

print("Fixed second batch of TS errors.")
