import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

pattern = re.compile(r'  app\.get\("/api/vibe/global-prompts", async \(req, res\) => \{\n    try \{\n      if \(!admin\.apps\.length\) return res\.json\(\{ success: true, data: \[\] \}\);\n      const db = admin\.firestore\(\);\n      const snapshot = await db\.collection\("vibe_global_prompts"\)\n        \.orderBy\("createdAt", "asc"\)\n        \.get\(\);\n      \n      const data = snapshot\.docs\.map\(doc => \(\{ id: doc\.id, \.\.\.doc\.data\(\) \}\)\);\n      res\.json\(\{ success: true, data \}\);\n    \} catch \(err: any\) \{\n      console\.error\("Failed to fetch global prompts:", err\);\n      res\.status\(500\)\.json\(\{ error: err\.message \}\);\n    \}\n  \}\);', re.MULTILINE)

replacement = """  app.get("/api/vibe/global-prompts", async (req, res) => {
    try {
      if (!admin.apps.length) return res.json({ success: true, data: [] });
      
      const cacheKey = "global_prompts";
      const cachedData = appCache.get(cacheKey);
      if (cachedData) {
         return res.json({ success: true, data: cachedData });
      }

      const db = admin.firestore();
      const snapshot = await db.collection("vibe_global_prompts")
        .orderBy("createdAt", "asc")
        .get();
      
      const data = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      
      appCache.set(cacheKey, data);
      res.json({ success: true, data });
    } catch (err: any) {
      console.error("Failed to fetch global prompts:", err);
      const staleData = appCache.getStale("global_prompts");
      if (staleData) {
         console.warn("Serving stale global prompts due to firestore error");
         return res.json({ success: true, data: staleData, stale: true });
      }
      res.status(500).json({ error: err.message });
    }
  });"""

new_content = pattern.sub(replacement, content)

if new_content == content:
    print("Failed to replace global prompts!")
else:
    print("Replaced global prompts successfully!")
    with open('server.ts', 'w') as f:
        f.write(new_content)
