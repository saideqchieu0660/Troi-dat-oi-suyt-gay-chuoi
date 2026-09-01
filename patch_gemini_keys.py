import re

with open("server.ts", "r") as f:
    content = f.read()

gemini_reset_block = """      let nonBannedKeys = geminiKeyStates.filter(s => s.status !== "HARD_LOCKED" && !s.is_banned);
      if (nonBannedKeys.length === 0) {
        geminiKeyStates.forEach(s => {
          s.status = "active";
          s.is_banned = false;
        });
        nonBannedKeys = geminiKeyStates;
      }
      selectedState = nonBannedKeys[0];"""
gemini_throw_block = """      let nonBannedKeys = geminiKeyStates.filter(s => s.status !== "HARD_LOCKED" && !s.is_banned);
      if (nonBannedKeys.length === 0) {
        throw new Error("All Gemini API keys are permanently BANNED or HARD_LOCKED.");
      }
      selectedState = nonBannedKeys[0];"""

if gemini_reset_block in content:
    content = content.replace(gemini_reset_block, gemini_throw_block)
    print("Patched Gemini key reset block")

with open("server.ts", "w") as f:
    f.write(content)
