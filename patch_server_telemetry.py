import sys

with open("server.ts", "r") as f:
    content = f.read()

# Add AsyncLocalStorage import
if "AsyncLocalStorage" not in content:
    content = content.replace('import express from "express";', 'import express from "express";\nimport { AsyncLocalStorage } from "async_hooks";\nconst asyncLocalStorage = new AsyncLocalStorage<any>();')

    # Add middleware right after app = express()
    content = content.replace('const app = express();', 'const app = express();\napp.use((req, res, next) => {\n  asyncLocalStorage.run({ res }, () => {\n    next();\n  });\n});')

    # Add header setting logic in _executeGenerateContentRoundRobinInternal
    # Target: if (state) handleGeminiError(state, err);
    # Actually, we want to set it on SUCCESS!
    # Inside Gemini success:
    gemini_success = """          const text = response?.text || response?.response?.text?.() || "";
          if (text) return text;"""
    gemini_success_new = """          const text = response?.text || response?.response?.text?.() || "";
          if (text) {
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "gemini");
                 store.res.setHeader("X-AI-Key", config.byokKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY"));
             }
             return text;
          }"""
    content = content.replace(gemini_success, gemini_success_new)

    # Inside Groq success:
    groq_success = """          const text = await executeGroqRequest(promptText, config);
          if (text) return text;"""
    groq_success_new = """          const text = await executeGroqRequest(promptText, config);
          if (text) {
             const store = asyncLocalStorage.getStore();
             if (store && store.res) {
                 store.res.setHeader("X-AI-Provider", "groq");
                 store.res.setHeader("X-AI-Key", "GROQ_KEY");
             }
             return text;
          }"""
    content = content.replace(groq_success, groq_success_new)

    with open("server.ts", "w") as f:
        f.write(content)
    print("Patched server.ts with telemetry headers")
else:
    print("Already patched server.ts")
