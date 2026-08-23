import sys
import re

with open("server.ts", "r") as f:
    content = f.read()

# Add node-cache import
if "import NodeCache" not in content:
    content = content.replace('import express from "express";', 'import express from "express";\nimport NodeCache from "node-cache";')

# Create cache instances
if "const myCache = new NodeCache" not in content:
    content = content.replace('const app = express();', 'const app = express();\nconst myCache = new NodeCache({ stdTTL: 60 });\nconst configCache = new NodeCache({ stdTTL: 600 });')

leaderboard_api = """
  app.get('/api/users/leaderboard', async (req, res, next) => {
    try {
      const cacheKey = 'leaderboard';
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      const q = db.collection('users').where('points', '>', 0).orderBy('points', 'desc').limit(10);
      const snapshot = await q.get();
      const data = [];
      snapshot.forEach(doc => data.push({ id: doc.id, ...doc.data() }));
      myCache.set(cacheKey, data, 300); // 5 minutes
      res.json(data);
    } catch (e) {
      next(e);
    }
  });
"""

if "/api/users/leaderboard" not in content:
    # Insert before the first config API
    content = content.replace('app.get("/api/config/health", (req, res) => {', leaderboard_api + '\n  app.get("/api/config/health", (req, res) => {')

with open("server.ts", "w") as f:
    f.write(content)
