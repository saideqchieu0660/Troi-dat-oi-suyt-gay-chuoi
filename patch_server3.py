import sys

with open("server.ts", "r") as f:
    content = f.read()

content = content.replace("finalError = err;", """if (state) handleGeminiError(state, err);
          finalError = err;""")
with open("server.ts", "w") as f:
    f.write(content)
