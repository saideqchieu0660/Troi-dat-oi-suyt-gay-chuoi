with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

old_dispatch = "states: [{ cardId: currentCard.id, isWeakCard: !remembered }]"
new_dispatch = "states: [{ cardId: currentCard.id, isWeakCard: !remembered, updatedAt: Date.now() }]"
content = content.replace(old_dispatch, new_dispatch)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)

print("Fixed VibeStudyRoom.tsx")
