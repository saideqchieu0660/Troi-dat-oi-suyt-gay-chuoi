import sys

with open("src/vibe-sandbox/sync/VibeSyncRescue.ts", "r") as f:
    content = f.read()

helper = """
// Helper to recursively remove undefined values to prevent Firestore crashes
export const removeUndefined = (obj: any): any => {
  if (Array.isArray(obj)) return obj.map(removeUndefined);
  if (obj !== null && typeof obj === 'object') {
    const newObj: any = {};
    for (const key in obj) {
      if (obj[key] !== undefined) {
        newObj[key] = removeUndefined(obj[key]);
      }
    }
    return newObj;
  }
  return obj;
};
"""

if "export const removeUndefined =" not in content:
    content = content.replace("export async function forceRescueMerge(", helper + "\nexport async function forceRescueMerge(")

content = content.replace("await setDoc(deckStateRef, {", "await setDoc(deckStateRef, removeUndefined({")
content = content.replace("lastUpdatedAt: Date.now()\n        }, { merge: true });", "lastUpdatedAt: Date.now()\n        }), { merge: true });")
content = content.replace("batch.set(ref, deck, { merge: true });", "batch.set(ref, removeUndefined(deck), { merge: true });")
content = content.replace("batch.set(pRef, mergedProfile, { merge: true });", "batch.set(pRef, removeUndefined(mergedProfile), { merge: true });")
content = content.replace("batch.set(ref, { states, deckId: dId, lastUpdatedAt: Date.now() }, { merge: true });", "batch.set(ref, removeUndefined({ states, deckId: dId, lastUpdatedAt: Date.now() }), { merge: true });")


with open("src/vibe-sandbox/sync/VibeSyncRescue.ts", "w") as f:
    f.write(content)
print("Patched VibeSyncRescue.ts")
