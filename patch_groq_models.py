import os

filepath = "src/lib/groq.ts"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace('PRIMARY: "llama-3.1-8b-instant"', 'PRIMARY: "llama3-8b-8192"')
content = content.replace('FALLBACK: "llama-3.3-70b-versatile"', 'FALLBACK: "llama3-8b-8192"')

with open(filepath, "w") as f:
    f.write(content)
print("Patched models in src/lib/groq.ts")
