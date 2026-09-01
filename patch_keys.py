import re

with open("server.ts", "r") as f:
    content = f.read()

groq_reset_block = """    if (nonBannedKeys.length === 0) {
      groqKeyStates.forEach(s => {
        s.status = "active";
        s.is_banned = false;
      });
      nonBannedKeys = groqKeyStates;
    }"""
groq_throw_block = """    if (nonBannedKeys.length === 0) {
      throw new Error("All Groq API keys are permanently BANNED or HARD_LOCKED.");
    }"""

gemini_reset_block = """    if (nonBannedKeys.length === 0) {
      geminiKeyStates.forEach(s => {
        s.status = "active";
        s.is_banned = false;
      });
      nonBannedKeys = geminiKeyStates;
    }"""
gemini_throw_block = """    if (nonBannedKeys.length === 0) {
      throw new Error("All Gemini API keys are permanently BANNED or HARD_LOCKED.");
    }"""

if groq_reset_block in content:
    content = content.replace(groq_reset_block, groq_throw_block)
    print("Patched Groq key reset block")

if gemini_reset_block in content:
    content = content.replace(gemini_reset_block, gemini_throw_block)
    print("Patched Gemini key reset block")

with open("server.ts", "w") as f:
    f.write(content)
