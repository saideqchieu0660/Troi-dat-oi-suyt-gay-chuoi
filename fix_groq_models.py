import sys

with open("src/lib/groq.ts", "r") as f:
    content = f.read()

content = content.replace('"llama-3.1-8b-instant"', '"llama3-8b-8192"')
content = content.replace('"llama-3.3-70b-versatile"', '"mixtral-8x7b-32768"')

with open("src/lib/groq.ts", "w") as f:
    f.write(content)
print("Fixed Groq models")
