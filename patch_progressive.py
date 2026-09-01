import re

with open("server.ts", "r") as f:
    content = f.read()

target = '  // AI Translate Definition for Flashcards (Vietnamese only)\n  app.post("/api/vibe/translate-definition"'

new_code = """  // AI Progressive Assist for Flashcards (Tier 1: Translate, Tier 2: Format, Tier 3: Explain)
  app.post("/api/vibe/card-progressive-assist", aiCooldownMiddleware, async (req, res, next) => {
    try {
      const { text, tier = 1, customPrompt = "" } = req.body;
      if (!text) {
        return res.status(400).json({ error: "Không có văn bản đầu vào." });
      }

      const cacheKey = "progressive_" + tier + "_" + Buffer.from(text + customPrompt).toString("base64").substring(0, 50);
      const cachedData = appCache.get(cacheKey);
      if (cachedData) {
         let traceLogs = [{ p: "system", s: "CACHE", m: `Truy xuất progressive assist tier ${tier} từ Cache (0đ)` }];
         const store = asyncLocalStorage.getStore();
         if (store && store.res) {
             store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
         }
         return res.json(cachedData);
      }

      let systemInstruction = `Bạn là một trợ lý AI thông minh chuyên xử lý thẻ học (Flashcard). 
Bạn PHẢI trả về dữ liệu đúng định dạng JSON object, tuyệt đối không kèm markdown (như \`\`\`json) hay text thừa nào khác.`;
      
      if (tier === 1) {
         systemInstruction += `\\nNHIỆM VỤ (TIER 1 - Dịch nghĩa):
1. Dịch phần giải nghĩa (definition) của các từ vựng sang tiếng Việt mượt mà.
2. TUYỆT ĐỐI KHÔNG dịch câu ví dụ (Example/e.g./Ex) sang tiếng Việt.
3. Trả về JSON với key "translation" chứa phần dịch.`;
      } else if (tier === 2) {
         systemInstruction += `\\nNHIỆM VỤ (TIER 2 - Định dạng & Dịch nghĩa):
1. ĐỊNH DẠNG (formatted_content): Trình bày lại văn bản gốc cho đẹp mắt (Dùng HTML/Markdown như <b>, <i>, <br>...). Sửa lỗi chính tả, xóa khoảng trắng thừa, trình bày có cấu trúc rõ ràng. Không tự ý cắt xén hay tóm tắt làm mất thông tin gốc.
2. DỊCH NGHĨA (translation): Dịch phần giải nghĩa sang tiếng Việt mượt mà (giữ nguyên câu ví dụ tiếng Anh nếu có).
3. Trả về JSON gồm 2 keys: "formatted_content" và "translation".`;
      } else {
         systemInstruction += `\\nNHIỆM VỤ (TIER 3 - Giải thích, Định dạng & Dịch nghĩa):
1. GIẢI THÍCH (explanation): Giải thích cặn kẽ về từ vựng, ngữ pháp hoặc trả lời câu hỏi.${customPrompt ? `\\nLƯU Ý ĐẶC BIỆT TỪ NGƯỜI DÙNG CHO PHẦN GIẢI THÍCH: "${customPrompt}"` : ""}
2. ĐỊNH DẠNG (formatted_content): Trình bày lại văn bản gốc cho đẹp mắt, cấu trúc rõ ràng.
3. DỊCH NGHĨA (translation): Dịch phần giải nghĩa sang tiếng Việt.
4. Trả về JSON gồm 3 keys: "explanation", "formatted_content", và "translation".`;
      }

      const prompt = `Văn bản gốc cần xử lý:\\n${text}`;

      let responseText = "";
      try {
        responseText = await executeGenerateContentRoundRobin(prompt, Object.assign({}, {
           temperature: 0.3,
           systemInstruction,
           responseMimeType: "application/json"
        }, { byokKey: req?.headers["x-byok-key"] , groqKey: req?.headers["x-groq-key"] }));
      } catch (err: any) {
        const staleData = appCache.getStale(cacheKey);
        if (staleData) {
           console.warn(`Serving stale progressive assist tier ${tier} due to AI error`);
           return res.json({ ...staleData, stale: true });
        }
        throw err;
      }

      const cleanedJSONStr = responseText.replace(/^```json\\n?|```$/g, '').trim();
      let parsedResponse;
      try {
         parsedResponse = JSON.parse(cleanedJSONStr);
      } catch(e) {
         throw new Error("AI trả về định dạng JSON không hợp lệ.");
      }

      appCache.set(cacheKey, parsedResponse);
      res.json(parsedResponse);
    } catch (error: any) {
      console.error("Progressive Assist Error:", error);
      next(error);
    }
  });

  // AI Translate Definition for Flashcards (Vietnamese only)
  app.post("/api/vibe/translate-definition" """

if target in content:
    content = content.replace(target, new_code)
    with open("server.ts", "w") as f:
        f.write(content)
    print("Patched Progressive API into server.ts")
else:
    print("Could not find target block in server.ts")

