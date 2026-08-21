const https = require('https');
const options = {
  hostname: 'api.groq.com',
  path: '/openai/v1/models',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${process.env.GROQ_API_KEY}`
  }
};
const req = https.request(options, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => console.log(data));
});
req.end();
