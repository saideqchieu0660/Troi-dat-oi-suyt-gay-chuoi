import sys

with open("server.ts", "r") as f:
    content = f.read()

# Replace all broken variations
content = content.replace("không bọc trong markdown code block (\\\\`\\\\`\\\\`).", "không bọc trong markdown code block (\\`\\`\\`).")
content = content.replace("không bọc trong markdown code block (```).", "không bọc trong markdown code block (\\`\\`\\`).")

with open("server.ts", "w") as f:
    f.write(content)
