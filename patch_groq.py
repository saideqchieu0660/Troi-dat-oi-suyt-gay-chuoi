import re

with open("server.ts", "r") as f:
    content = f.read()

# First replace the entire Groq block in _executeGenerateContentRoundRobinInternal
old_groq_block = """      } else if (provider === "groq") {
        try {
          const text = await executeGroqRequest(promptText, config);
          if (text) {
             traceLogs.push({ p: "groq", s: "OK", k: "GROQ_KEY" });
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", "GROQ_KEY");
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }
             return text;
          }
        } catch (err: any) {
          const errMsg = (err?.message || "").toLowerCase();
          let isRateLimit = false;
          if (errMsg.includes("401") || errMsg.includes("403") || errMsg.includes("unauthorized") || errMsg.includes("invalid api key")) {
             console.warn("[groq] API Key invalid/unauthorized. Triggering 1-hour cooldown for Groq.");
             providerCooldowns.groq = Date.now() + 3600000;
          } else if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             console.warn("[groq] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.groq = Date.now() + COOLDOWN_MS;
             isRateLimit = true;
          } else {
             console.warn("[groq] Provider failed, trying fallback...", err?.message);
          }
          traceLogs.push({ p: "groq", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 200) });
          finalError = err;
        }
      }"""

new_groq_block = """      } else if (provider === "groq") {
        let state: KeyState | undefined;
        try {
          let groqKey = config.groqKey;
          if (!groqKey) {
             const keyInfo = getGroqKey();
             groqKey = keyInfo.key;
             state = keyInfo.state;
          }
          const text = await executeGroqRequest(promptText, { ...config, groqKey });
          if (text) {
             const keyInfo = config.groqKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY");
             traceLogs.push({ p: "groq", s: "OK", k: keyInfo });
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }
             return text;
          }
        } catch (err: any) {
          const errMsg = (err?.message || "").toLowerCase();
          let isRateLimit = false;
          
          if (state) {
              handleGroqError(state, err);
          } else {
              if (errMsg.includes("401") || errMsg.includes("403") || errMsg.includes("unauthorized") || errMsg.includes("invalid api key")) {
                 console.warn("[groq] BYOK API Key invalid/unauthorized.");
              } else if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
                 console.warn("[groq] BYOK Rate limit/Overload detected.");
                 isRateLimit = true;
              }
          }

          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             isRateLimit = true;
          }
          
          traceLogs.push({ p: "groq", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 200) });
          finalError = err;
        }
      }"""

if old_groq_block in content:
    content = content.replace(old_groq_block, new_groq_block)
    with open("server.ts", "w") as f:
        f.write(content)
    print("Patched Groq rotation logic successfully!")
else:
    print("Could not find old_groq_block in server.ts")

