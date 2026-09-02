import re

with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "r") as f:
    content = f.read()

# Fix 1: Add updatedAt: Date.now() to the pushed update
old_push = "(globalThis as any)._vibeCardStateUpdates.push({ cardId: card.id, isWeakCard: shouldBeHard });"
new_push = "(globalThis as any)._vibeCardStateUpdates.push({ cardId: card.id, isWeakCard: shouldBeHard, updatedAt: Date.now() });"
content = content.replace(old_push, new_push)

# Fix 2: Navigate to weak mode when restoring backup
old_nav = "navigate(`/study/${deck.id}`);"
new_nav = "navigate(`/study/${deck.id}?mode=weak`);"
content = content.replace(old_nav, new_nav)

with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "w") as f:
    f.write(content)

print("Fixed VibeStudyEntryModal.tsx")
