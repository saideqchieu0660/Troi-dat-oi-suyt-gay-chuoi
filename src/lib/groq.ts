export const GROQ_MODELS = {
  PRIMARY: "openai/gpt-oss-120b",
  FALLBACK: "openai/gpt-oss-120b"
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
        max_tokens: config.maxOutputTokens !== undefined ? Math.min(config.maxOutputTokens, 2048) : undefined,
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

  const MAX_RETRIES = 3; // Tăng retry lên 3 nhưng với backoff
  
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
       return await makeRequest(GROQ_MODELS.PRIMARY);
    } catch (err: any) {

       console.warn(`[groq] Primary model ${GROQ_MODELS.PRIMARY} failed (Attempt ${attempt}/${MAX_RETRIES}):`, err.message);
       
       if (err.message.includes('401') || err.message.includes('403')) {
           throw new Error(`Groq Key Invalid/Unauthorized (401/403): ${err.message}`);
       }

       
       const isRateLimitOrServerError = err.message.includes('429') || err.message.includes('503') || err.message.includes('500');
       
       if (attempt === MAX_RETRIES) {
          console.warn(`[groq] Falling back to ${GROQ_MODELS.FALLBACK}...`);
          try {
             return await makeRequest(GROQ_MODELS.FALLBACK);
          } catch (fallbackErr: any) {
             throw new Error(`Both Primary and Fallback models failed. Fallback error: ${fallbackErr.message}`);
          }
       }
       
       // Exponential backoff logic with jitter
       const baseDelay = isRateLimitOrServerError ? 2000 : 1000;
       const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 500;
       console.log(`[groq] Waiting ${delay.toFixed(0)}ms before retry...`);
       await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw new Error("Failed to execute Groq request.");
}
