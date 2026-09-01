import re

with open("server.ts", "r") as f:
    content = f.read()

old = r"""      let q = db\.collection\('vibe_decks'\); // GLOBAL POOL VIBE
      const snapshot = await q\.get\(\);
      const data = \[\];
      snapshot\.forEach\(doc => \{
         const docData = doc\.data\(\);
         if \(!deckId \|\| doc\.id === deckId\) \{
            data\.push\(\{ id: doc\.id, \.\.\.docData \}\);
         \}
      \}\);"""

new = """      // --- LẤY DANH SÁCH CATEGORY BỊ ẨN ---
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
         let subj = "Chưa phân loại";
         if (docData.subject) {
             subj = typeof docData.subject === "string" ? docData.subject : JSON.stringify(docData.subject);
         }
         subj = subj.trim();
         
         // Nếu deck nằm trong category bị ẩn, BỎ QUA KHÔNG TRẢ VỀ API (chỉ ngoại trừ có deckId cụ thể thì có thể trả về)
         if (!deckId && hiddenCategories.includes(subj)) {
             return; // Bỏ qua
         }

         if (!deckId || doc.id === deckId) {
            data.push({ id: doc.id, ...docData });
         }
      });"""

content = re.sub(old, new, content)

with open("server.ts", "w") as f:
    f.write(content)
print("Patched!")
