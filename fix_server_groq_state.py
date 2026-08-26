import sys

with open("server.ts", "r") as f:
    content = f.read()

# Remove the line `if (state) handleGeminiError(state, err);` inside the Groq block
groq_err_block = """          traceLogs.push({ p: "groq", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 50) });
          if (state) handleGeminiError(state, err);
          finalError = err;"""

groq_err_block_fixed = """          traceLogs.push({ p: "groq", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 50) });
          finalError = err;"""

content = content.replace(groq_err_block, groq_err_block_fixed)

with open("server.ts", "w") as f:
    f.write(content)
print("Fixed Groq state error")
