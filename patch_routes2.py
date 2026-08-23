import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

# Make sure all routes have `next`
content = re.sub(
    r'app\.(get|post|put|delete)\("([^"]+)",\s*(?:express\.json\([^)]*\),\s*)?async \((req, res|req: express\.Request, res: express\.Response)\) => \{',
    lambda m: m.group(0).replace(m.group(3), m.group(3) + ", next"),
    content
)

def replace_status(match):
    catch_var = match.group(1)
    body = match.group(2)
    
    if "res.status(" not in body and "res.json({ error:" not in body:
        return match.group(0)
    if "appCache.getStale" in body:
        return match.group(0)
        
    # we just find the last res.status(...) or return res.status(...) and replace it
    new_body = re.sub(r'(?:return\s+)?res\.status\(\d+\)\.json\([^;]+\);?', f'next({catch_var});', body)
    return f"catch ({catch_var}) {{{new_body}}}"

content = re.sub(r'catch \(([^)]+)\) \{([^}]+)\}', replace_status, content)

with open('server.ts', 'w') as f:
    f.write(content)
print("Routes patched 2")
