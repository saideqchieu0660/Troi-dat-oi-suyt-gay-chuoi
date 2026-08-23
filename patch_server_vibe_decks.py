import sys

with open("server.ts", "r") as f:
    content = f.read()

vibe_decks_api = """
  app.get('/api/vibe/decks', async (req, res, next) => {
    try {
      const { userId, deckId } = req.query;
      if (!userId) return res.status(400).json({ error: "Missing userId" });
      
      const cacheKey = `vibe_decks_${userId}_${deckId || 'all'}`;
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      let q = db.collection('vibe_decks').where('ownerId', '==', userId);
      const snapshot = await q.get();
      const data = [];
      snapshot.forEach(doc => {
         const docData = doc.data();
         if (!deckId || doc.id === deckId) {
            data.push({ id: doc.id, ...docData });
         }
      });
      
      myCache.set(cacheKey, data, 60); // Cache 60s
      res.json(data);
    } catch (e) {
      next(e);
    }
  });
"""

if "/api/vibe/decks" not in content:
    content = content.replace('app.get("/api/vibe/keys-status",', vibe_decks_api + '\n  app.get("/api/vibe/keys-status",')

with open("server.ts", "w") as f:
    f.write(content)
