import sys

with open("server.ts", "r") as f:
    content = f.read()

helper = """
    // Helper to recursively remove undefined values
    const removeUndefined = (obj: any): any => {
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

# Insert the helper inside app.post("/api/sync/push" before const batch = db.batch();
target_line = "    const batch = db.batch();"
new_lines = helper + "\n" + target_line

if "const removeUndefined =" not in content:
    content = content.replace(target_line, new_lines)

# Now, we just need to make sure item.payload is cleaned.
# Replace `for (const item of itemsToProcess) {` with cleaning
target_loop = "    for (const item of itemsToProcess) {"
new_loop = """    for (let item of itemsToProcess) {
      if (item.payload) {
        item.payload = removeUndefined(item.payload);
      }
"""

if "item.payload = removeUndefined(item.payload);" not in content:
    content = content.replace(target_loop, new_loop)

with open("server.ts", "w") as f:
    f.write(content)
print("Patched server.ts")
