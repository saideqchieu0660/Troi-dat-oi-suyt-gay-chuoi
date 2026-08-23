import sys

with open('server.ts', 'r') as f:
    content = f.read()

import_statement = 'import { executeGroqRequest } from "./src/lib/groq";\n'
if import_statement not in content:
    content = content.replace('import dotenv from "dotenv";', import_statement + 'import dotenv from "dotenv";')

target_block = """        try {
          const groqKeyToUse = config.groqKey || process.env.GROQ_API_KEY;
          const messages = [];
          if (config.systemInstruction) {
             messages.push({ role: "system", content: config.systemInstruction });
          }
          messages.push({ role: "user", content: promptText });
          
          let groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
             method: "POST",
             headers: {
                "Authorization": `Bearer ${groqKeyToUse}`,
                "Content-Type": "application/json"
             },
             body: JSON.stringify({
                model: "llama-3.3-70b-versatile",
                messages: messages,
                temperature: config.temperature !== undefined ? config.temperature : 0.7,
                max_tokens: config.maxOutputTokens !== undefined ? config.maxOutputTokens : undefined,
                response_format: isJsonMode ? { type: "json_object" } : undefined
             })
          });

          if (!groqRes.ok) {
             console.warn(`[groq] 70B failed (${groqRes.status}), falling back to 8B instant...`);
             groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
                method: "POST",
                headers: {
                   "Authorization": `Bearer ${groqKeyToUse}`,
                   "Content-Type": "application/json"
                },
                body: JSON.stringify({
                   model: "mixtral-8x7b-32768",
                   messages: messages,
                   temperature: config.temperature !== undefined ? config.temperature : 0.7,
                   max_tokens: config.maxOutputTokens !== undefined ? config.maxOutputTokens : undefined,
                   response_format: isJsonMode ? { type: "json_object" } : undefined
                })
             });
             
             if (!groqRes.ok) {
                const errText = await groqRes.text();
                throw new Error(`Groq API Error: ${groqRes.status} - ${errText}`);
             }
          }
          const groqData = await groqRes.json();
          const text = groqData.choices?.[0]?.message?.content || "";
          if (text) return text;"""

replacement = """        try {
          const text = await executeGroqRequest(promptText, config);
          if (text) return text;"""

content = content.replace(target_block, replacement)

with open('server.ts', 'w') as f:
    f.write(content)
