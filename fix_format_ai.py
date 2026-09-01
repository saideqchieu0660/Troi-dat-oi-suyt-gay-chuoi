import re

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "r") as f:
    content = f.read()

old_format_1 = """onClick={handleFormatAI}
                             disabled={isFormatting}"""
new_format_1 = """onClick={(e) => { e.stopPropagation(); handleProgressiveAssist(2); }}
                             disabled={activeTier !== null || isFormatting}"""
content = content.replace(old_format_1, new_format_1)


with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "w") as f:
    f.write(content)

print("Fixed handleFormatAI references!")
