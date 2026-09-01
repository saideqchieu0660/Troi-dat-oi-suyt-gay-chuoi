import re

with open("server.ts", "r") as f:
    content = f.read()

# Replace the beginning of the loop
old_loop_start = """  let finalError: any = null;
  let traceLogs: any[] = [];
  for (const provider of activeProviders) {"""
new_loop_start = """  let finalError: any = null;
  let traceLogs: any[] = [];
  let attemptedProviders: string[] = [];
  for (const provider of activeProviders) {
    attemptedProviders.push(provider);"""

content = content.replace(old_loop_start, new_loop_start)

# Replace gemini success block
old_gemini_success = """             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "gemini");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }"""
new_gemini_success = """             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "gemini");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
                 if (attemptedProviders.length > 1) {
                     store.res.setHeader("X-AI-Fallback", attemptedProviders.join("->"));
                 }
             }"""

content = content.replace(old_gemini_success, new_gemini_success)

# Replace groq success block
old_groq_success = """             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
             }"""
new_groq_success = """             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", keyInfo);
                 store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
                 if (attemptedProviders.length > 1) {
                     store.res.setHeader("X-AI-Fallback", attemptedProviders.join("->"));
                 }
             }"""

content = content.replace(old_groq_success, new_groq_success)

with open("server.ts", "w") as f:
    f.write(content)
print("Patched fallback headers!")
