import sys

with open("server.ts", "r") as f:
    content = f.read()

content = content.replace("model: aiModelToUse", "model: aiModelToUse,\n            forcedProvider: req.body.forcedProvider")
with open("server.ts", "w") as f:
    f.write(content)
