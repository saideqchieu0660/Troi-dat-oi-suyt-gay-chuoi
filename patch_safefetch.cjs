const fs = require('fs');
let code = fs.readFileSync('src/utils/safeFetch.ts', 'utf8');

code = code.replace(/const byokKey = typeof window !== 'undefined' \? localStorage.getItem\("henosis_gemini_key"\) : null;/g, `const geminiKey = typeof window !== 'undefined' ? localStorage.getItem("henosis_gemini_key") : null;
  const groqKey = typeof window !== 'undefined' ? localStorage.getItem("henosis_groq_key") : null;
  const cerebrasKey = typeof window !== 'undefined' ? localStorage.getItem("henosis_cerebras_key") : null;`);

code = code.replace(/if \(isAiEndpoint && !byokKey\) {/g, `if (isAiEndpoint && !geminiKey && !groqKey) {`);

code = code.replace(/if \(byokKey\) {[\s\S]*?finalOptions.headers = headers;\n  }/g, `if (geminiKey) {
    const headers = new Headers(finalOptions.headers || {});
    if (!headers.has("x-byok-key")) headers.set("x-byok-key", geminiKey);
    finalOptions.headers = headers;
  }
  if (groqKey) {
    const headers = new Headers(finalOptions.headers || {});
    if (!headers.has("x-groq-key")) headers.set("x-groq-key", groqKey);
    finalOptions.headers = headers;
  }
  if (cerebrasKey) {
    const headers = new Headers(finalOptions.headers || {});
    if (!headers.has("x-cerebras-key")) headers.set("x-cerebras-key", cerebrasKey);
    finalOptions.headers = headers;
  }`);

fs.writeFileSync('src/utils/safeFetch.ts', code);
