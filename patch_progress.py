import sys

with open("src/vibe-sandbox/sync/VibeProgressSyncManager.ts", "r") as f:
    content = f.read()

if "import { removeUndefined } from \"./VibeSyncRescue\";" not in content:
    content = content.replace('import { StoreManager }', 'import { removeUndefined } from "./VibeSyncRescue";\nimport { StoreManager }')

content = content.replace("await setDoc(docRef, {", "await setDoc(docRef, removeUndefined({")
content = content.replace("updatedAt: local.updatedAt \n      }, { merge: true });", "updatedAt: local.updatedAt \n      }), { merge: true });")
content = content.replace("updatedAt: local.updatedAt // Push the exact time we modified it locally\n      }, { merge: true });", "updatedAt: local.updatedAt // Push the exact time we modified it locally\n      }), { merge: true });")

with open("src/vibe-sandbox/sync/VibeProgressSyncManager.ts", "w") as f:
    f.write(content)
print("Patched VibeProgressSyncManager.ts")
