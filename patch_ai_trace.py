import sys

# --- PATCH SERVER.TS ---
with open("server.ts", "r") as f:
    server_content = f.read()

# Add let traceLogs: any[] = [];
if "let traceLogs: any[] = [];" not in server_content:
    server_content = server_content.replace(
        "let finalError: any = null;",
        "let finalError: any = null;\n  let traceLogs: any[] = [];"
    )

# Update Gemini success
gemini_success_old = """          if (text) {
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "gemini");
                 store.res.setHeader("X-AI-Key", config.byokKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY"));
             }
             return text;
          }"""
gemini_success_new = """          if (text) {
             const keyInfo = config.byokKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY");
             traceLogs.push({ p: "gemini", s: "OK", k: keyInfo });
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "gemini");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }
             return text;
          }"""
server_content = server_content.replace(gemini_success_old, gemini_success_new)

# Update Gemini error
gemini_err_old = """          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("quota") || errMsg.includes("overloaded") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504")) {
             console.warn("[gemini] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.gemini = Date.now() + COOLDOWN_MS;
          } else {
             console.warn("[gemini] Provider failed, trying fallback...", err?.message);
          }
          if (state) handleGeminiError(state, err);
          finalError = err;"""
gemini_err_new = """          let isRateLimit = false;
          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("quota") || errMsg.includes("overloaded") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504")) {
             console.warn("[gemini] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.gemini = Date.now() + COOLDOWN_MS;
             isRateLimit = true;
          } else {
             console.warn("[gemini] Provider failed, trying fallback...", err?.message);
          }
          traceLogs.push({ p: "gemini", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 50) });
          if (state) handleGeminiError(state, err);
          finalError = err;"""
server_content = server_content.replace(gemini_err_old, gemini_err_new)

# Update Groq success
groq_success_old = """          if (text) {
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", "GROQ_KEY");
             }
             return text;
          }"""
groq_success_new = """          if (text) {
             traceLogs.push({ p: "groq", s: "OK", k: "GROQ_KEY" });
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", "GROQ_KEY");
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }
             return text;
          }"""
server_content = server_content.replace(groq_success_old, groq_success_new)

# Update Groq error
groq_err_old = """          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             console.warn("[groq] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.groq = Date.now() + COOLDOWN_MS;
          } else {
             console.warn("[groq] Provider failed, trying fallback...", err?.message);
          }
          if (state) handleGeminiError(state, err);
          finalError = err;"""
groq_err_new = """          let isRateLimit = false;
          if (errMsg.includes("429") || errMsg.includes("too many") || errMsg.includes("503") || errMsg.includes("500") || errMsg.includes("504") || errMsg.includes("rate limit")) {
             console.warn("[groq] Rate limit/Overload detected. Triggering 1-minute cooldown.");
             providerCooldowns.groq = Date.now() + COOLDOWN_MS;
             isRateLimit = true;
          } else {
             console.warn("[groq] Provider failed, trying fallback...", err?.message);
          }
          traceLogs.push({ p: "groq", s: isRateLimit ? "RATE_LIMIT" : "ERROR", m: (err?.message || "").substring(0, 50) });
          if (state) handleGeminiError(state, err);
          finalError = err;"""
server_content = server_content.replace(groq_err_old, groq_err_new)

# Update throw finalError
throw_old = 'throw finalError || new Error("All API Providers failed");'
throw_new = """  if (finalError) {
      const store = asyncLocalStorage.getStore();
      if (store && store.res) {
          store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
      }
  }
  throw finalError || new Error("All API Providers failed");"""
server_content = server_content.replace(throw_old, throw_new)

with open("server.ts", "w") as f:
    f.write(server_content)


# --- PATCH APICLIENT.TS ---
with open("src/utils/apiClient.ts", "r") as f:
    api_content = f.read()

trace_parser = """const extractAITrace = (response: Response) => {
  try {
    const aiTraceB64 = response.headers.get("X-AI-Trace");
    if (aiTraceB64 && typeof window !== "undefined") {
        const traceStr = atob(aiTraceB64);
        const traces = JSON.parse(traceStr);
        for (const t of traces) {
            const providerName = t.p.toUpperCase();
            if (t.s === 'OK') {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI DISPATCHER] Xử lý THÀNH CÔNG bởi ${providerName} (Key: ${t.k})`, type: 'success' }
                }));
            } else if (t.s === 'RATE_LIMIT') {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI DISPATCHER] ${providerName} BỊ RATE LIMIT / QUÁ TẢI. Tự động xoay sang API dự phòng...`, type: 'warn' }
                }));
            } else {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI DISPATCHER] ${providerName} LỖI: ${t.m}. Xoay sang API dự phòng...`, type: 'error' }
                }));
            }
        }
        return true;
    }
  } catch(e) {}
  return false;
};
"""

if "const extractAITrace" not in api_content:
    api_content = api_content.replace("export async function safeRequest", trace_parser + "\nexport async function safeRequest")

# Replace old telemetry intercept with new one
old_telemetry = """        // --- AI Telemetry Log Intercept ---
        try {
          const aiProvider = response.headers.get("X-AI-Provider");
          const aiKey = response.headers.get("X-AI-Key");
          if (aiProvider && typeof window !== "undefined") {
            const providerName = aiProvider.toUpperCase();
            window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
              detail: {
                message: `[AI DISPATCHER] Xử lý thành công bởi ${providerName} (Key sử dụng: ${aiKey || "Không xác định"})`,
                type: 'success'
              }
            }));
          }
        } catch(e) {}"""

new_telemetry = """        // --- AI Telemetry Log Intercept ---
        const hasTrace = extractAITrace(response);
        if (!hasTrace) {
          try {
            const aiProvider = response.headers.get("X-AI-Provider");
            const aiKey = response.headers.get("X-AI-Key");
            if (aiProvider && typeof window !== "undefined") {
              const providerName = aiProvider.toUpperCase();
              window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                detail: {
                  message: `[AI DISPATCHER] Xử lý THÀNH CÔNG bởi ${providerName} (Key sử dụng: ${aiKey || "Không xác định"})`,
                  type: 'success'
                }
              }));
            }
          } catch(e) {}
        }"""
api_content = api_content.replace(old_telemetry, new_telemetry)

# Add to error handlers:
client_err_target = """      // Client errors (400 - 499, except 429 and 408) - abort early without repeating
      if (response.status >= 400 && response.status < 500) {"""
client_err_new = """      extractAITrace(response);
      // Client errors (400 - 499, except 429 and 408) - abort early without repeating
      if (response.status >= 400 && response.status < 500) {"""
if "extractAITrace(response);" not in api_content.split("// Client errors")[0].split("}")[-1]:
    api_content = api_content.replace(client_err_target, client_err_new)

with open("src/utils/apiClient.ts", "w") as f:
    f.write(api_content)
print("Trace telemetry patched successfully.")
