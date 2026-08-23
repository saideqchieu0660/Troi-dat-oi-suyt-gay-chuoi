export const GROQ_MODELS = {
  PRIMARY: "llama2-70b-4096",
  FALLBACK: "mixtral-8x7b-32768"
};

interface GroqConfig {
  groqKey?: string;
  systemInstruction?: string;
  temperature?: number;
  maxOutputTokens?: number;
  responseMimeType?: string;
}

export async function executeGroqRequest(promptText: string, config: GroqConfig = {}): Promise<string> {
  const groqKey = config.groqKey || process.env.GROQ_API_KEY;
  if (!groqKey) {
    throw new Error("GROQ API key not configured.");
  }

  const messages: { role: string, content: string }[] = [];
  if (config.systemInstruction) {
    messages.push({ role: "system", content: config.systemInstruction });
  }
  messages.push({ role: "user", content: promptText });

  const isJsonMode = config.responseMimeType === "application/json";

  const makeRequest = async (model: string) => {
    const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${groqKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: config.temperature !== undefined ? config.temperature : 0.7,
        max_tokens: config.maxOutputTokens !== undefined ? config.maxOutputTokens : undefined,
        response_format: isJsonMode ? { type: "json_object" } : undefined
      })
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Groq API Error: ${res.status} - ${errorText}`);
    }
    
    const data = await res.json();
    return data.choices?.[0]?.message?.content || "";
  };

  const MAX_RETRIES = 2;
  
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
       return await makeRequest(GROQ_MODELS.PRIMARY);
    } catch (err: any) {
       console.warn(`[groq] Primary model ${GROQ_MODELS.PRIMARY} failed (Attempt ${attempt}/${MAX_RETRIES}):`, err.message);
       if (attempt === MAX_RETRIES) {
          console.warn(`[groq] Falling back to ${GROQ_MODELS.FALLBACK}...`);
          try {
             return await makeRequest(GROQ_MODELS.FALLBACK);
          } catch (fallbackErr: any) {
             throw new Error(`Both Primary and Fallback models failed. Fallback error: ${fallbackErr.message}`);
          }
       }
       // Wait before retry
       await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }
  
  throw new Error("Failed to execute Groq request.");
}
