import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

# Replace `res.status(500).json({ error: err.message ... })` with `next(err)`
content = re.sub(r'(?:return\s+)?res\.status\(\d+\)\.json\(\{\s*error:\s*(err|error)\.message[^}]*\}\);?', r'next(\1);', content)

# Replace `res.status(500).json({ error: true, message: err.message ... })` with `next(err)`
content = re.sub(r'(?:return\s+)?res\.status\(\d+\)\.json\(\{\s*error:\s*true,\s*message:\s*(err|error)\.message[^}]*\}\);?', r'next(\1);', content)

# Replace `res.status(500).json({ error: error.message || "..." })`
content = re.sub(r'(?:return\s+)?res\.status\(\d+\)\.json\(\{\s*error:\s*(?:true,\s*message:\s*)?(err|error)\.message\s*\|\|[^}]*\}\);?', r'next(\1);', content)

# Replace `res.status(500).json({ error: err.message, stack: err.stack })`
content = re.sub(r'(?:return\s+)?res\.status\(\d+\)\.json\(\{\s*error:\s*(err|error)\.message,\s*stack:\s*\1\.stack\s*\}\);?', r'next(\1);', content)

with open('server.ts', 'w') as f:
    f.write(content)
print("Patched status 500")
