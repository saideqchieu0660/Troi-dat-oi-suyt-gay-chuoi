import sys

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "r") as f:
    content = f.read()

target = """    try {
      const res = await safeFetch("/api/automation/format-card", {"""

new_target = """    try {
      const { safeRequest } = await import("../utils/apiClient");
      const res = await safeRequest("/api/automation/format-card", {"""

content = content.replace(target, new_target)
with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "w") as f:
    f.write(content)
print("Patched format-card")
