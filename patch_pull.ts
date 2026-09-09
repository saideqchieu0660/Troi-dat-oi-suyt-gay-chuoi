import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/sync/VibeSyncEngine.ts', 'utf8');

const pullMethod = `
  async pullLatestCardStates(uid: string): Promise<number> {
    if (!navigator.onLine) return 0;
    
    try {
      // 1. Get last pull time
      const lastPullTime = (await get(\`vibe_last_pull_time_\${uid}\`)) as number || 0;
      
      // 2. Query Firestore
      const deckStatesRef = collection(db, "users", uid, "vibe_deckStates");
      const q = query(
          deckStatesRef, 
          where("lastUpdatedAt", ">", lastPullTime)
      );
      
      const snapshot = await getDocs(q);
      if (snapshot.empty) {
          await set(\`vibe_last_pull_time_\${uid}\`, Date.now());
          return 0;
      }

      let updatedCardsCount = 0;
      const { CardStateManager } = await import("../../lib/CardStateManager");
      const serverPullTime = Date.now();

      // 3. Process changes
      for (const docSnap of snapshot.docs) {
          const data = docSnap.data();
          if (data.states) {
              for (const [cardId, statePayload] of Object.entries<any>(data.states)) {
                  // Only apply if the server's state is newer than our last pull
                  if (statePayload.lastUpdatedAt && statePayload.lastUpdatedAt > lastPullTime) {
                      updatedCardsCount++;
                      
                      // Update idb-keyval so getDecks() merges it
                      const merged = { ...statePayload, uid, deckId: data.deckId, cardId, lastUpdatedAt: serverPullTime };
                      await set(\`vibe_cardstate_\${uid}_\${cardId}\`, merged);

                      // Update CardStateManager memory/IDB SOT
                      const patch = {
                          mastery: statePayload.mastery,
                          isHard: typeof statePayload.isWeakCard === "boolean" ? statePayload.isWeakCard : statePayload.isHard,
                          repetitionCount: statePayload.repetitionCount,
                          interval: statePayload.interval,
                          easeFactor: statePayload.easeFactor,
                          nextReviewDate: statePayload.nextReviewDate,
                          lastPointAwarded: statePayload.lastPointAwarded || 0,
                          updatedAt: serverPullTime
                      };
                      await CardStateManager.updateCardState(uid, cardId, patch);
                  }
              }
          }
      }

      // 4. Update last pull time
      await set(\`vibe_last_pull_time_\${uid}\`, serverPullTime);
      
      if (updatedCardsCount > 0) {
         // Fire an event so UI can show a toast or refresh
         if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('vibe-card-states-pulled', { detail: { count: updatedCardsCount } }));
         }
         this.notify();
      }
      return updatedCardsCount;
    } catch (e) {
      console.warn("[VibeSyncEngine] pullLatestCardStates error:", e);
      return 0;
    }
  }
`;

if (!content.includes('pullLatestCardStates')) {
   content = content.replace('async syncNow() {', pullMethod + '\n  async syncNow() {');
   writeFileSync('src/vibe-sandbox/sync/VibeSyncEngine.ts', content);
   console.log("Patched successfully");
} else {
   console.log("Already patched");
}
