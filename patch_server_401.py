import sys
import re

with open("server.ts", "r") as f:
    content = f.read()

target = """          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             console.warn("[groq] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.groq = Date.now() + COOLDOWN_MS;
             isRateLimit = true;
          } else {"""

replacement = """          if (errMsg.includes("401") || errMsg.includes("403") || errMsg.includes("unauthorized") || errMsg.includes("invalid api key")) {
             console.warn("[groq] API Key invalid/unauthorized. Triggering 1-hour cooldown for Groq.");
             providerCooldowns.groq = Date.now() + 3600000;
          } else if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             console.warn("[groq] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.groq = Date.now() + COOLDOWN_MS;
             isRateLimit = true;
          } else {"""

content = content.replace(target, replacement)

with open("server.ts", "w") as f:
    f.write(content)
print("Patched server.ts")
