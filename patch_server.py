import sys

with open("server.ts", "r") as f:
    content = f.read()

old_code = """  app.get('/api/users/leaderboard', async (req, res, next) => {
    try {
      const cacheKey = 'leaderboard';
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      const q = db.collection('users').where('points', '>', 0).orderBy('points', 'desc').limit(10);"""

new_code = """  app.get('/api/users/leaderboard', async (req, res, next) => {
    try {
      const cacheKey = 'leaderboard';
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      if (!admin.apps.length) {
        return res.status(503).json({ error: "Firebase Admin not initialized" });
      }
      const db = admin.firestore();

      const q = db.collection('users').where('points', '>', 0).orderBy('points', 'desc').limit(10);"""

content = content.replace(old_code, new_code)

with open("server.ts", "w") as f:
    f.write(content)
