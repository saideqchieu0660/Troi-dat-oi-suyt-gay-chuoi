import re

with open("src/vibe-sandbox/VibeBackupRestoreX.tsx", "r") as f:
    content = f.read()

# Make sure CardStateManager is imported
if "import { CardStateManager }" not in content:
    content = 'import { CardStateManager } from "../lib/CardStateManager";\n' + content

# Replace the enqueueChange with updateCardState
old_sync = """            // Push qua VibeSyncEngine để đồng bộ server
            await VibeSyncEngine.enqueueChange({
                type: "UPSERT_CARD_STATE",
                payload: {
                    uid: currentUser.id,
                    cardId: card.id,
                    isWeakCard: shouldBeHard
                }
            }).catch(err => console.warn("Queue ignored:", err));"""
new_sync = """            // Cập nhật CardStateManager đồng bộ để Dashboard / Room đọc được ngay
            await CardStateManager.updateCardState(currentUser.id, card.id, { isHard: shouldBeHard });
            // Cập nhật server
            await VibeSyncEngine.enqueueChange({
                type: "UPSERT_CARD_STATE",
                payload: {
                    uid: currentUser.id,
                    cardId: card.id,
                    isWeakCard: shouldBeHard,
                    updatedAt: Date.now()
                }
            }).catch(err => console.warn("Queue ignored:", err));"""
content = content.replace(old_sync, new_sync)

with open("src/vibe-sandbox/VibeBackupRestoreX.tsx", "w") as f:
    f.write(content)

print("Patched VibeBackupRestoreX.tsx!")
