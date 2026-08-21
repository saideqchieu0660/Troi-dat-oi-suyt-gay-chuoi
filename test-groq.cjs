const https = require('https');
const data = JSON.stringify({
  model: "llama3-70b-8192",
  messages: [{ role: "user", content: "hello" }],
  temperature: 0.7,
  max_completion_tokens: undefined
});
const options = {
  hostname: 'api.groq.com',
  path: '/openai/v1/chat/completions',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.GROQ_API_KEY || 'invalid_key'}`,
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};
const req = https.request(options, res => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => console.log(res.statusCode, body));
});
req.write(data);
req.end();
