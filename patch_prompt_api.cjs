const fs = require('fs');
let code = fs.readFileSync('server.ts', 'utf-8');

const target = `  app.post("/api/vibe/generate-prompt", express.json(), async (req, res, next) => {
    try {
      const { description } = req.body;
      if (!description) return res.status(400).json({ error: "Missing description" });

      const systemInstruction = \`Bạn là một chuyên gia viết Prompt (Prompt Engineer). 
Nhiệm vụ của bạn là viết một đoạn hướng dẫn ngắn gọn (system prompt snippet) để chèn vào ngữ cảnh của AI, nhằm định hướng AI trả lời theo một phong cách hoặc yêu cầu cụ thể mà người dùng muốn tạo nhãn.

Ví dụ: 
- Người dùng nhập: "Giải thích kiểu GenZ"
- Bạn viết: "Hãy giải thích bằng ngôn ngữ của GenZ, sử dụng các từ lóng (slang) phổ biến, cách nói chuyện hài hước, trẻ trung, nhưng vẫn đảm bảo giữ được ý nghĩa học thuật cốt lõi."

Hãy trả về TRỰC TIẾP đoạn prompt đó, không giải thích, không bọc trong markdown block. Giữ nó ngắn gọn (khoảng 2-4 câu), sắc bén và tập trung vào phong cách/yêu cầu.\`;

      const contents = [{ role: "user", parts: [{ text: \`Mô tả nhãn/phong cách người dùng muốn tạo: \${description}\` }] }];
      const responseText = await executeGenerateContentRoundRobin(contents, Object.assign({}, {
        systemInstruction,
        temperature: 0.7,
        model: "gemini-3.6-flash"
      }, { byokKey: req?.headers["x-byok-key"] , groqKey: req?.headers["x-groq-key"] }));

      res.json({ success: true, prompt: responseText.trim() });
    } catch (err: any) {
      console.error("Failed to generate prompt:", err);
      next(err);
    }
  });`;

const replacement = `  app.post("/api/vibe/generate-prompt", express.json(), async (req, res, next) => {
    try {
      const { title, rawPrompt, history = [], newMessage } = req.body;
      
      // Fallback cho logic cũ nếu UI chưa cập nhật gọi kiểu mới
      const description = req.body.description || title;
      
      if (!description && !rawPrompt && !newMessage) return res.status(400).json({ error: "Missing inputs" });

      const systemInstruction = \`Bạn là một chuyên gia Prompt Engineer thượng thừa. 
Nhiệm vụ của bạn là tối ưu hóa, cấu trúc lại và viết ra một System Prompt hoàn chỉnh (để cấp cho AI khác) dựa trên mong muốn thô của người dùng.
- LUÔN TRẢ VỀ TRỰC TIẾP nội dung Prompt. Không cần giải thích thêm, không bọc trong markdown code block (\`\`\`).
- Nếu người dùng yêu cầu chỉnh sửa (trong lịch sử chat), hãy tinh chỉnh Prompt trước đó theo đúng yêu cầu mới.\`;

      let promptText = "";
      
      // Khởi tạo ngữ cảnh gốc
      promptText += \`--- THÔNG TIN GỐC TỪ NGƯỜI DÙNG ---\\n\`;
      promptText += \`Tên/Tiêu đề Nhãn: \${title || "Không có"}\\n\`;
      promptText += \`Ý tưởng Prompt thô (Raw Prompt): \${rawPrompt || description || "Không có"}\\n\\n\`;
      
      if (history.length === 0 && !newMessage) {
        promptText += \`YÊU CẦU: Dựa vào thông tin trên, hãy viết ra một System Prompt thật chuyên nghiệp, rõ ràng, giúp AI hiểu chính xác nó cần đóng vai trò gì và trả lời như thế nào.\`;
      } else {
        promptText += \`--- LỊCH SỬ TINH CHỈNH ---\\n\`;
        history.forEach((msg: any) => {
            promptText += \`[\${msg.role === 'model' ? 'AI Prompt Đã Tạo' : 'Người Dùng Yêu Cầu Sửa'}]: \${msg.content}\\n\`;
        });
        promptText += \`\\n--- YÊU CẦU CHỈNH SỬA MỚI NHẤT ---\\n\`;
        promptText += \`Người dùng: \${newMessage}\\n\`;
        promptText += \`YÊU CẦU: Hãy áp dụng yêu cầu mới nhất này vào bản Prompt trước đó để tạo ra phiên bản hoàn thiện cuối cùng.\`;
      }

      const contents = [{ role: "user", parts: [{ text: promptText }] }];
      
      const responseText = await executeGenerateContentRoundRobin(contents, Object.assign({}, {
        systemInstruction,
        temperature: 0.7,
        model: "gemini-3.6-flash"
      }, { byokKey: req?.headers["x-byok-key"] , groqKey: req?.headers["x-groq-key"] }));

      res.json({ success: true, prompt: responseText.trim() });
    } catch (err: any) {
      console.error("Failed to generate prompt:", err);
      next(err);
    }
  });`;

if (code.includes('const { description } = req.body;')) {
    code = code.replace(target, replacement);
    fs.writeFileSync('server.ts', code);
    console.log("Patched server.ts successfully");
} else {
    console.log("Could not find target block in server.ts");
}
