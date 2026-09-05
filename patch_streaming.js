const fs = require('fs');

let serverTs = fs.readFileSync('server.ts', 'utf8');

const streamFunc = `
async function executeGenerateStreamRoundRobin(res: any, contents: any, config: any = {}): Promise<void> {
  const isJsonMode = config.responseMimeType === "application/json";
  let promptText = "";
  if (typeof contents === "string") {
    promptText = contents;
  } else if (Array.isArray(contents)) {
    promptText = contents.map(c => {
       if (c.text) return c.text;
       if (c.inlineData) return "[Image data attached - Supported on Gemini only]";
       return JSON.stringify(c);
    }).join("\\n");
  }

  const forbiddenKeywords = [
    "hack", "exploit", "bypass", "malware", "virus", "phishing",
    "nsfw", "porn", "violence", "kill", "murder", "suicide"
  ];
  const promptLower = promptText.toLowerCase();
  for (const keyword of forbiddenKeywords) {
    if (promptLower.includes(keyword)) {
      throw new Error(\`[Content Safety] Request blocked due to prohibited keyword: \${keyword}.\`);
    }
  }

  const hasGeminiKey = !!config.byokKey || !!process.env.GEMINI_API_KEY;
  const hasGroqKey = !!config.groqKey || !!process.env.GROQ_API_KEY;

  const now = Date.now();
  const hasGemini = hasGeminiKey && (now > providerCooldowns.gemini);
  const hasGroq = hasGroqKey && (now > providerCooldowns.groq);

  let activeProviders: string[] = [];
  if (hasGemini && hasGroq) {
     globalRoundRobinCounter++;
     if (globalRoundRobinCounter % 2 === 0) {
        activeProviders = ["gemini", "groq"];
     } else {
        activeProviders = ["groq", "gemini"];
     }
  } else if (hasGroq) {
     activeProviders = ["groq"];
  } else if (hasGemini) {
     activeProviders = ["gemini"];
  } else {
     activeProviders = hasGroqKey ? ["groq", "gemini"] : ["gemini", "groq"];
  }

  let finalError: any = null;
  let traceLogs: any[] = [];
  const attemptedProviders: string[] = [];

  for (const provider of activeProviders) {
    attemptedProviders.push(provider);
    try {
      if (provider === "gemini") {
        let state: any;
        let ai;
        if (config.byokKey) {
           const h = getSpoofedHeaders();
           ai = new GoogleGenAI({
             apiKey: config.byokKey,
             httpOptions: {
                headers: {
                  "User-Agent": h["User-Agent"],
                  "X-Forwarded-For": h["X-Forwarded-For"]
                }
             }
           });
        } else {
           const clientInfo = getGeminiClient();
           ai = clientInfo.ai;
           state = clientInfo.state;
        }

        const resultStream = await ai.models.generateContentStream({
          model: config.model || "gemini-3.6-flash",
          contents: promptText,
          config: {
            ...(config.systemInstruction ? { systemInstruction: config.systemInstruction } : {}),
            ...(config.temperature !== undefined ? { temperature: config.temperature } : {}),
            ...(config.maxOutputTokens !== undefined ? { maxOutputTokens: config.maxOutputTokens } : {}),
            ...(isJsonMode ? { responseMimeType: "application/json" } : {})
          }
        });

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        let hasStarted = false;
        for await (const chunk of resultStream) {
          if (!hasStarted) {
             const keyInfo = config.byokKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY");
             traceLogs.push({ p: "gemini", s: "OK", k: keyInfo });
             res.write(\`data: \${JSON.stringify({ type: "trace", data: traceLogs })}\\n\\n\`);
             hasStarted = true;
          }
          if (chunk.text) {
             res.write(\`data: \${JSON.stringify({ type: "chunk", text: chunk.text })}\\n\\n\`);
          }
        }
        res.write(\`data: \${JSON.stringify({ type: "done" })}\\n\\n\`);
        res.end();
        return;
      } else if (provider === "groq") {
        // Fallback to Groq without streaming, but wrap it in SSE so client doesn't break
        let state: KeyState | undefined;
        let groqKey = config.groqKey;
        if (!groqKey) {
           const keyInfo = getGroqKey();
           groqKey = keyInfo.key;
           state = keyInfo.state;
        }
        const text = await executeGroqRequest(promptText, { ...config, groqKey });
        
        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");
        
        const keyInfo = config.groqKey ? "BYOK_KEY" : (state ? state.maskedKey : "SERVER_KEY");
        traceLogs.push({ p: "groq", s: "OK", k: keyInfo });
        res.write(\`data: \${JSON.stringify({ type: "trace", data: traceLogs })}\\n\\n\`);
        res.write(\`data: \${JSON.stringify({ type: "chunk", text: text })}\\n\\n\`);
        res.write(\`data: \${JSON.stringify({ type: "done" })}\\n\\n\`);
        res.end();
        return;
      }
    } catch (err: any) {
      console.warn(\`[stream] Provider \${provider} failed:\`, err.message);
      if (res.headersSent) {
         res.write(\`data: \${JSON.stringify({ type: "error", error: err.message })}\\n\\n\`);
         res.end();
         return;
      }
      finalError = err;
    }
  }

  throw finalError || new Error("All AI providers failed for streaming.");
}
`;

if (!serverTs.includes('executeGenerateStreamRoundRobin')) {
  const insertPos = serverTs.indexOf('async function _executeGenerateContentRoundRobinInternal');
  serverTs = serverTs.slice(0, insertPos) + streamFunc + '\n' + serverTs.slice(insertPos);
  fs.writeFileSync('server.ts', serverTs);
}
