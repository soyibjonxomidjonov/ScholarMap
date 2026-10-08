import os
import re

src_dir = 'scholarmap-frontend/src'
for filename in os.listdir(src_dir):
    if filename.endswith('.tsx') and filename not in ['App.tsx', 'main.tsx']:
        filepath = os.path.join(src_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix inline onClick="..." to onClick={() => { ... }}
        content = re.sub(r'onClick="([^"]+)"', r'onClick={() => { \1 }}', content)
        content = re.sub(r'onChange="([^"]+)"', r'onChange={() => { \1 }}', content)
        content = re.sub(r'onInput="([^"]+)"', r'onInput={() => { \1 }}', content)
        
        # Basic fixes for unclosed tags from naive HTML conversion
        content = content.replace('class=', 'className=')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
print('JSX files cleaned up')
