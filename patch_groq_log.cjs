const fs = require('fs');
let code = fs.readFileSync('server.ts', 'utf8');

code = code.replace(/console\.warn\(\`\\[groq\\] 70B failed \(\\\${groqRes\.status}\), falling back to 8B instant\.\.\.\`\);/g, `const errText = await groqRes.text();
             console.warn(\`[groq] 70B failed (\${groqRes.status}): \${errText}, falling back to 8B instant...\`);`);

fs.writeFileSync('server.ts', code);
