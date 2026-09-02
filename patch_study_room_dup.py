import re

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

# We want to remove handleLocalStateUpdate and its listener.
# The code looks like:
#     const handleLocalStateUpdate = (e: any) => { ... }
#     window.addEventListener("vibe-card-states-updated", handleLocalStateUpdate);
#     const handleBackupRestored = () => { ... }
#     window.addEventListener("vibe-backup-restored", handleBackupRestored);
#     return () => {
#       window.removeEventListener("vibe-card-states-updated", handleLocalStateUpdate);
#       window.removeEventListener("vibe-backup-restored", handleBackupRestored);
#     };

old_chunk = """    const handleLocalStateUpdate = (e: any) => {
      if (e.detail && e.detail.states) {
        setPersonalCardStates(prev => {
          const next = [...prev];
          e.detail.states.forEach((s: any) => {
            const idx = next.findIndex(p => p.id === s.cardId);
            if (idx >= 0) {
              next[idx] = { ...next[idx], isWeakCard: s.isWeakCard, updatedAt: Date.now() };
            } else {
              next.push({ id: s.cardId, isWeakCard: s.isWeakCard, updatedAt: Date.now() });
            }
          });
          return next;
        });
      }
    };
    window.addEventListener("vibe-card-states-updated", handleLocalStateUpdate);
    
    const handleBackupRestored = () => {"""

new_chunk = """    const handleBackupRestored = () => {"""

content = content.replace(old_chunk, new_chunk)

cleanup_old = """      window.removeEventListener("vibe-card-states-updated", handleLocalStateUpdate);
      window.removeEventListener("vibe-backup-restored", handleBackupRestored);"""
cleanup_new = """      window.removeEventListener("vibe-backup-restored", handleBackupRestored);"""
content = content.replace(cleanup_old, cleanup_new)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)

print("Removed duplicate listener")
