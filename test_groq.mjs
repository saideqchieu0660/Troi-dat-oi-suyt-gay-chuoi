import fetch from "node-fetch";

async function testGroq() {
  const keys = [
    process.env.GROQ_API_KEY, process.env.VITE_GROQ_API_KEY, process.env.GROQ_API_KEY_1
  ].filter(Boolean);
  
  if (keys.length === 0) {
    console.log("No GROQ keys found in env.");
    return;
  }
  
  const key = keys[0];
  console.log("Using key prefix:", key.slice(0, 8));
  
  const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${key}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "llama3-8b-8192",
      messages: [{role: "user", content: "Hello"}],
      temperature: 0.7
    })
  });
  
  console.log("Status:", res.status);
  console.log("Response:", await res.text());
}
testGroq();
