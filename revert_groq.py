import os

filepath = "src/lib/groq.ts"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace('max_tokens: config.maxOutputTokens !== undefined ? Math.min(config.maxOutputTokens, 2048) : undefined,', 'max_tokens: config.maxOutputTokens !== undefined ? config.maxOutputTokens : undefined,')

with open(filepath, "w") as f:
    f.write(content)
print("Reverted max_tokens in src/lib/groq.ts")
