import re

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

old_code = """        // Update local object to reflect new mastery for subsequent reviews in the same session
        currentCard.mastery = oldMastery + diff;"""
new_code = """        // Update local object to reflect new mastery for subsequent reviews in the same session
        currentCard.mastery = oldMastery + diff;
        currentCard.isHard = !remembered;"""
content = content.replace(old_code, new_code)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)

print("Patched handleMark for isHard")
