import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

pattern = re.compile(r'      \} else if \(provider === "groq"\) \{\n        try \{\n          const groqKeyToUse.*?\n          if \(text\) return text;', re.DOTALL)

replacement = """      } else if (provider === "groq") {
        try {
          const text = await executeGroqRequest(promptText, config);
          if (text) return text;"""

new_content = pattern.sub(replacement, content)

if new_content == content:
    print("Failed to replace!")
else:
    print("Replaced successfully!")
    with open('server.ts', 'w') as f:
        f.write(new_content)
