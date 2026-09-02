with open("src/vibe-sandbox/VibeBackupRestoreX.tsx", "r") as f:
    content = f.read()

old_push = "globalThis._vibeCardStateUpdates.push({ cardId: card.id, isWeakCard: shouldBeHard });"
new_push = "globalThis._vibeCardStateUpdates.push({ cardId: card.id, isWeakCard: shouldBeHard, updatedAt: Date.now() });"
content = content.replace(old_push, new_push)

with open("src/vibe-sandbox/VibeBackupRestoreX.tsx", "w") as f:
    f.write(content)

print("Fixed VibeBackupRestoreX.tsx")
