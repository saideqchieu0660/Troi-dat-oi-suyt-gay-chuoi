import os

with open("server.ts", "r") as f:
    content = f.read()

# Patch 1
content = content.replace(
    '''await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ usageCount: admin.firestore.FieldValue.increment(1) });
      const h = getSpoofedHeaders();''',
    '''await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ usageCount: admin.firestore.FieldValue.increment(1) });
      selectedKey.usageCount = (selectedKey.usageCount || 0) + 1;
      const h = getSpoofedHeaders();'''
)

# Patch 2
content = content.replace(
    '''if (isYellow) {
        await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ status: "YELLOW", recoveryTime: Date.now() + 30000 });
        console.warn(`Vibe Rotator: Key ${selectedKey.id} hit YELLOW. Global pause for 30s...`);''',
    '''if (isYellow) {
        await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ status: "YELLOW", recoveryTime: Date.now() + 30000 });
        selectedKey.status = "YELLOW";
        selectedKey.recoveryTime = Date.now() + 30000;
        console.warn(`Vibe Rotator: Key ${selectedKey.id} hit YELLOW. Global pause for 30s...`);'''
)

# Patch 3
content = content.replace(
    '''} else if (isRed) {
        await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ status: "RED" });
        console.warn(`Vibe Rotator: Key ${selectedKey.id} hit RED (Banned). Re-routing immediately...`);''',
    '''} else if (isRed) {
        await db.collection("vibe_api_keys_pool").doc(selectedKey.id).update({ status: "RED" });
        selectedKey.status = "RED";
        console.warn(`Vibe Rotator: Key ${selectedKey.id} hit RED (Banned). Re-routing immediately...`);'''
)

with open("server.ts", "w") as f:
    f.write(content)
