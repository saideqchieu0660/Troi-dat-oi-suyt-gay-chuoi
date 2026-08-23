import sys

with open('server.ts', 'r') as f:
    content = f.read()

batch_endpoint = """   // API Config Batch Endpoint
   app.get("/api/config/batch", async (req, res) => {
     res.setHeader("Cache-Control", "public, max-age=300"); // 5 minutes cache on HTTP layer as well
     await Promise.all([refreshApiToggles(), refreshAIPrompts()]);
     return res.json({
       toggles: { groqEnabled: false, openRouterEnabled: false, geminiEnabled: true, deepInfraEnabled: false }, // matching the behavior of api-toggles
       prompts: globalAIPrompts || {}
     });
   });
"""

target = '   app.get("/api/config/api-toggles", async (req, res) => {'
if target in content and batch_endpoint not in content:
    content = content.replace(target, batch_endpoint + "\n" + target)
    with open('server.ts', 'w') as f:
        f.write(content)
    print("Added batch endpoint")
else:
    print("Already added or target not found")
