import sys

with open("server.ts", "r") as f:
    content = f.read()

# Refactor ai-prompts
old_prompts = """  app.get("/api/config/ai-prompts", async (req, res, next) => {
      try {
         const doc = await db.collection("system_config").doc("ai_prompts").get();
         if (doc.exists) {
            res.json(doc.data());
         } else {
            res.json({});
         }
      } catch (err: any) {
         next(err);
      }
   });"""

new_prompts = """  app.get("/api/config/ai-prompts", async (req, res, next) => {
      try {
         const cached = configCache.get("ai-prompts");
         if (cached) return res.json(cached);
         
         const doc = await db.collection("system_config").doc("ai_prompts").get();
         const data = doc.exists ? doc.data() : {};
         configCache.set("ai-prompts", data);
         res.json(data);
      } catch (err: any) {
         next(err);
      }
   });"""

content = content.replace(old_prompts, new_prompts)

# Refactor api-toggles
old_toggles = """  app.get("/api/config/api-toggles", async (req, res, next) => { 
      try {
         const doc = await db.collection("system_config").doc("api_toggles").get();
         if (doc.exists) {
            res.json(doc.data());
         } else {
            res.json({});
         }
      } catch (err: any) {
         next(err);
      }
   });"""

new_toggles = """  app.get("/api/config/api-toggles", async (req, res, next) => { 
      try {
         const cached = configCache.get("api-toggles");
         if (cached) return res.json(cached);
         
         const doc = await db.collection("system_config").doc("api_toggles").get();
         const data = doc.exists ? doc.data() : {};
         configCache.set("api-toggles", data);
         res.json(data);
      } catch (err: any) {
         next(err);
      }
   });"""

content = content.replace(old_toggles, new_toggles)

with open("server.ts", "w") as f:
    f.write(content)
