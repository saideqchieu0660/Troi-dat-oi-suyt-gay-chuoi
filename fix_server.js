const fs = require('fs');
let code = fs.readFileSync('server.ts', 'utf-8');
code = code.replace("không bọc trong markdown code block (```).", "không bọc trong markdown code block (\\\`\\\`\\\`).");
fs.writeFileSync('server.ts', code);
