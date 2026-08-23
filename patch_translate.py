import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

pattern = re.compile(r'  app\.post\("/api/vibe/translate-definition", aiCooldownMiddleware, async \(req, res, next\) => \{.*?\n  \}\);', re.DOTALL)
match = pattern.search(content)

if match:
    print("Found match!")
    target = match.group(0)
    replacement = """  app.post("/api/vibe/translate-definition", aiCooldownMiddleware, async (req, res, next) => {
    try {
      const { text } = req.body;
      if (!text) {
        return res.status(400).json({ error: "No text provided for translation." });
      }
      
      const cacheKey = "translate_" + Buffer.from(text).toString("base64").substring(0, 50);
      const cachedData = appCache.get(cacheKey);
      if (cachedData) {
         return res.json({ translatedText: cachedData.translatedText });
      }

      const prompt = `Bạn là một trợ lý dịch thuật tiếng Anh chuyên nghiệp. Nhiệm vụ của bạn là dịch phần giải nghĩa (definition) của các từ vựng sang tiếng Việt.

YÊU CẦU BẮT BUỘC TỐI THƯỢNG:
1. NẾU CÓ CÂU VÍ DỤ (Example/e.g./Ex), BẠN TUYỆT ĐỐI KHÔNG ĐƯỢC DỊCH CÂU VÍ DỤ ĐÓ SANG TIẾNG VIỆT. Câu ví dụ phải được GIỮ NGUYÊN 100% bằng tiếng Anh. Mọi thao tác dịch ví dụ đều bị nghiêm cấm.
2. Dịch nghĩa tiếng Việt phải mượt mà, chính xác ngữ cảnh.
3. CHỈ TRẢ VỀ CHUỖI VĂN BẢN ĐẦU RA. KHÔNG GIẢI THÍCH, KHÔNG THÊM BẤT KỲ LỜI CHÀO HAY GHI CHÚ NÀO.

Định dạng văn bản gốc:
${text}`;

      let responseText = "";
      try {
        responseText = await executeGenerateContentRoundRobin(prompt, Object.assign({}, {
           temperature: 0.3
        }, { byokKey: req?.headers["x-byok-key"] , groqKey: req?.headers["x-groq-key"] }));
      } catch (geminiError: any) {
        const staleData = appCache.getStale(cacheKey);
        if (staleData) {
           console.warn("Serving stale translate definition due to AI quota/error");
           return res.json({ translatedText: staleData.translatedText, stale: true });
        }
        throw geminiError;
      }
      
      const cleanedTranslation = responseText.trim().replace(/^["']|["']$/g, "");
      
      appCache.set(cacheKey, { translatedText: cleanedTranslation });
      res.json({ translatedText: cleanedTranslation });
    } catch (error: any) {
      console.error("Translate Definition Error:", error);
      next(error);
    }
  });"""
    content = content.replace(target, replacement)
    with open('server.ts', 'w') as f:
        f.write(content)
else:
    print("Not found")
