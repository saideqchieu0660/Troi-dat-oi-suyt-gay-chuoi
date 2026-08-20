const fs = require('fs');
let code = fs.readFileSync('src/App.tsx', 'utf8');
const lines = code.split('\n');
lines.splice(139, 8, 
'  const handleSaveGeminiKey = async () => {',
'    if (geminiKeyInput.trim()) {',
'      const keyStr = geminiKeyInput.trim();',
'      localStorage.setItem("henosis_gemini_key", keyStr);',
'      toast("Đã lưu Google API Key trên máy thành công!");',
'      setGeminiKeyInput(keyStr);',
'    }',
'  };'
);
fs.writeFileSync('src/App.tsx', lines.join('\n'));
