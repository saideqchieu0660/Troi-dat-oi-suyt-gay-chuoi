import sys

with open("server.ts", "r") as f:
    content = f.read()

active_providers_logic = """  let activeProviders: string[] = [];
  if (config.forcedProvider === "groq") {
     activeProviders = ["groq"];
  } else if (config.forcedProvider === "gemini") {
     activeProviders = ["gemini"];
  } else if (hasGemini && hasGroq) {"""

content = content.replace("  let activeProviders: string[] = [];\n  if (hasGemini && hasGroq) {", active_providers_logic)

# Make sure agent3/chat passes forcedProvider
content = content.replace("useProModel: useProModel", "useProModel: req.body.useProModel, forcedProvider: req.body.forcedProvider")
# Wait, req.body.useProModel is in VibeStudyRoom.tsx.
# In server.ts, we need to pass req.body.forcedProvider to executeGenerateContentRoundRobin.
# Let's see agent3/chat:
