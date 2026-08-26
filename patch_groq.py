import sys
import re

with open("src/lib/groq.ts", "r") as f:
    content = f.read()

# Update models
content = content.replace('"llama3-8b-8192"', '"llama-3.1-8b-instant"')
content = content.replace('"mixtral-8x7b-32768"', '"llama-3.3-70b-versatile"')

# Add 401/403 abort
abort_logic = """
       console.warn(`[groq] Primary model ${GROQ_MODELS.PRIMARY} failed (Attempt ${attempt}/${MAX_RETRIES}):`, err.message);
       
       if (err.message.includes('401') || err.message.includes('403')) {
           throw new Error(`Groq Key Invalid/Unauthorized (401/403): ${err.message}`);
       }
"""
content = content.replace("       console.warn(`[groq] Primary model ${GROQ_MODELS.PRIMARY} failed (Attempt ${attempt}/${MAX_RETRIES}):`, err.message);", abort_logic)

with open("src/lib/groq.ts", "w") as f:
    f.write(content)

print("Patched groq.ts")
