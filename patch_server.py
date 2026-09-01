import os

with open("server.ts", "r") as f:
    content = f.read()

old_logic = """    try {
      const { userId, deckId } = req.query;
      if (!userId) return res.status(400).json({ error: "Missing userId" });
      
      if (!admin.apps.length) {
        return res.status(503).json({ error: "Firebase Admin not initialized" });
      }
      const db = admin.firestore();
      const cacheKey = `vibe_decks_${userId}_${deckId || 'all'}`;
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      let q = db.collection('vibe_decks'); // GLOBAL POOL VIBE
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
    } catch (e) {"""

new_logic = """    try {
      const { userId, deckId } = req.query;
      if (!userId) return res.status(400).json({ error: "Missing userId" });
      
      if (!admin.apps.length) {
        return res.status(503).json({ error: "Firebase Admin not initialized" });
      }
      const db = admin.firestore();
      const cacheKey = `vibe_decks_${userId}_${deckId || 'all'}`;
      const cached = myCache.get(cacheKey);
      if (cached) return res.json(cached);

      // --- LẤY DANH SÁCH CATEGORY BỊ ẨN ---
      let hiddenCategories: string[] = [];
      try {
        const hiddenSnap = await db.collection("vibe_settings").doc("dashboard_config").get();
        if (hiddenSnap.exists) {
           hiddenCategories = hiddenSnap.data()?.hiddenCategories || [];
        }
      } catch (err) {
        console.error("Failed to fetch hidden categories", err);
      }

      let q = db.collection('vibe_decks'); // GLOBAL POOL VIBE
      const snapshot = await q.get();
      const data: any[] = [];
      snapshot.forEach(doc => {
         const docData = doc.data();
         
         // Lọc các deck có subject bị ẩn
         let subj = "general";
         if (docData.subject) {
             subj = typeof docData.subject === "string" ? docData.subject : JSON.stringify(docData.subject);
         }
         subj = subj.trim();
         // Nếu deck nằm trong category bị ẩn, BỎ QUA KHÔNG TRẢ VỀ API (chỉ ngoại trừ có deckId cụ thể thì có thể trả về, nhưng tạm thời chặn sạch)
         if (!deckId && hiddenCategories.includes(subj)) {
             return; // Bỏ qua
         }

         if (!deckId || doc.id === deckId) {
            data.push({ id: doc.id, ...docData });
         }
      });
      
      myCache.set(cacheKey, data, 60); // Cache 60s
      res.json(data);
    } catch (e) {"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open("server.ts", "w") as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old logic in server.ts")
