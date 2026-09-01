import os

with open("server.ts", "r") as f:
    content = f.read()

content = content.replace('m: (err?.message || "").substring(0, 50)', 'm: (err?.message || "").substring(0, 200)')

with open("server.ts", "w") as f:
    f.write(content)
print("Patched!")
