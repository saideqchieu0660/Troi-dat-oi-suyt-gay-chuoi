import sys

with open("server.ts", "r") as f:
    content = f.read()

target = """  app.get('/api/vibe/decks', async (req, res, next) => {
    try {
      const { userId, deckId } = req.query;
      if (!userId) return res.status(400).json({ error: "Missing userId" });
      
      const cacheKey = `vibe_decks_${userId}_${deckId || 'all'}`;
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      let q = db.collection('vibe_decks').where('ownerId', '==', userId);"""

new_target = """  app.get('/api/vibe/decks', async (req, res, next) => {
    try {
      const { userId, deckId } = req.query;
      if (!userId) return res.status(400).json({ error: "Missing userId" });
      
      if (!admin.apps.length) {
        return res.status(503).json({ error: "Firebase Admin not initialized" });
      }
      const db = admin.firestore();

      const cacheKey = `vibe_decks_${userId}_${deckId || 'all'}`;
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      let q = db.collection('vibe_decks').where('ownerId', '==', userId);"""

content = content.replace(target, new_target)

with open("server.ts", "w") as f:
    f.write(content)
print("Fixed db reference in /api/vibe/decks")
