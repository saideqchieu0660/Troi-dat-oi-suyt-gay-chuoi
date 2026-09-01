import os

with open("src/lib/groq.ts", "r") as f:
    content = f.read()

content = content.replace('max_tokens: config.maxOutputTokens !== undefined ? config.maxOutputTokens : undefined,', 'max_tokens: config.maxOutputTokens !== undefined ? Math.min(config.maxOutputTokens, 2048) : undefined,')

with open("src/lib/groq.ts", "w") as f:
    f.write(content)
print("Patched max tokens!")
