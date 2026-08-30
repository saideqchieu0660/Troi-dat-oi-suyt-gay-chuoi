import sys

helper = """
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

# Patch VibeSyncRescue.ts
with open("src/vibe-sandbox/sync/VibeSyncRescue.ts", "r") as f:
    content = f.read()

if "export const removeUndefined =" not in content:
    content = helper + "\n" + content
    with open("src/vibe-sandbox/sync/VibeSyncRescue.ts", "w") as f:
        f.write(content)

# Patch VibeProgressSyncManager.ts
with open("src/vibe-sandbox/sync/VibeProgressSyncManager.ts", "r") as f:
    content2 = f.read()

if "import { removeUndefined }" not in content2:
    content2 = 'import { removeUndefined } from "./VibeSyncRescue";\n' + content2
    with open("src/vibe-sandbox/sync/VibeProgressSyncManager.ts", "w") as f:
        f.write(content2)

