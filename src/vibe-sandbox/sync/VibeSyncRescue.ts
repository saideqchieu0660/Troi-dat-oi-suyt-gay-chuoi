import { get, set, keys } from "idb-keyval";
import { db } from "../../lib/firebase";
import { collection, doc, getDocs, getDoc, writeBatch, query, where } from "firebase/firestore";
import { store } from "../../lib/store";
import { auth } from "../../lib/firebase";

export async function forceMergeRescue(): Promise<string> {
  const user = store.getCurrentUser() || auth.currentUser;
  if (!user) throw new Error("No authenticated user.");
  const uid = typeof user === 'string' ? user : (user as any).uid || (user as any).id;
  if (!uid) throw new Error("Could not determine user ID.");

  const log: string[] = [];
  log.push("Bắt đầu quy trình Force Merge LWW (Last-Write-Wins)...");

  try {
    // 1. GOM LOCAL DATA
    log.push("Đang thu thập dữ liệu Local (IndexedDB)...");
    const allLocalKeys = await keys();
    const localDecks: Record<string, any> = {};
    const localCardStates: Record<string, any> = {};
    let localProfile: any = null;

    for (const key of allLocalKeys as string[]) {
      if (key.startsWith("vibe_deck_")) {
        localDecks[key.replace("vibe_deck_", "")] = await get(key);
      } else if (key.startsWith(`vibe_cardstate_${uid}_`)) {
        localCardStates[key.replace(`vibe_cardstate_${uid}_`, "")] = await get(key);
      } else if (key === `vibe_profile_${uid}`) {
        localProfile = await get(key);
      }
    }

    // 2. GOM CLOUD DATA
    log.push("Đang tải dữ liệu từ Cloud (Firestore)...");
    const { limit } = await import("firebase/firestore");
    const cloudDecks: Record<string, any> = {};
    const qDecks = query(collection(db, "vibe_decks"), where("ownerId", "==", uid), limit(500));
    console.log("[FIRESTORE READ] VibeSyncRescue.ts: getDocs on vibe_decks");
    const cloudDecksSnap = await getDocs(qDecks);
    cloudDecksSnap.forEach(d => {
       cloudDecks[d.id] = { id: d.id, ...d.data() };
    });

    let cloudProfile: any = null;
    const pDoc = await getDoc(doc(db, "users", uid));
    if (pDoc.exists()) cloudProfile = pDoc.data();

    const cloudCardStates: Record<string, any> = {};
    console.log("[FIRESTORE READ] VibeSyncRescue.ts: getDocs on cardsState");
    const cStatesSnap = await getDocs(query(collection(db, "users", uid, "cardsState"), limit(2000)));
    cStatesSnap.forEach(d => {
      cloudCardStates[d.id] = { cardId: d.id, ...d.data() };
    });

    // 3. MERGE THE TRUTH
    log.push("Tiến hành gộp dữ liệu...");
    const mergedDecks: Record<string, any> = {};
    const allDeckIds = new Set([...Object.keys(localDecks), ...Object.keys(cloudDecks)]);
    for (const dId of allDeckIds) {
      const local = localDecks[dId];
      const cloud = cloudDecks[dId];
      
      if (local && cloud) {
        const localTime = local.lastUpdatedAt || 0;
        const cloudTime = cloud.lastUpdatedAt || 0;
        // Ưu tiên bản nào mới hơn
        mergedDecks[dId] = localTime > cloudTime ? local : cloud;
      } else {
        mergedDecks[dId] = local || cloud;
      }
    }

    const mergedCardStates: Record<string, any> = {};
    const allCardStateIds = new Set([...Object.keys(localCardStates), ...Object.keys(cloudCardStates)]);
    for (const cId of allCardStateIds) {
      const local = localCardStates[cId];
      const cloud = cloudCardStates[cId];
      
      if (local && cloud) {
        const localTime = local.updatedAt || local.lastUpdatedAt || 0;
        const cloudTime = cloud.updatedAt || cloud.lastUpdatedAt || 0;
        
        // Nếu bằng nhau hoặc không rõ, so sánh điểm Mastery
        if (localTime === cloudTime) {
           const localM = local.mastery || 0;
           const cloudM = cloud.mastery || 0;
           mergedCardStates[cId] = localM > cloudM ? local : cloud;
        } else {
           mergedCardStates[cId] = localTime > cloudTime ? local : cloud;
        }
      } else {
        mergedCardStates[cId] = local || cloud;
      }
    }

    let mergedProfile = cloudProfile || {};
    if (localProfile) {
      const localTime = localProfile.lastUpdatedAt || 0;
      const cloudTime = cloudProfile?.lastUpdatedAt || 0;
      if (localTime > cloudTime) {
         mergedProfile = { ...cloudProfile, ...localProfile };
      } else {
         mergedProfile = { ...localProfile, ...cloudProfile };
      }
    }

    // 4. LƯU LẠI MASTER DATA XUỐNG LOCAL VÀ ĐẨY LÊN CLOUD
    log.push("Đang đồng bộ bản Master lên Cloud và Local...");
    
    // Đẩy Local
    for (const [dId, deck] of Object.entries(mergedDecks)) {
      await set(`vibe_deck_${dId}`, deck);
    }
    for (const [cId, state] of Object.entries(mergedCardStates)) {
      await set(`vibe_cardstate_${uid}_${cId}`, state);
      // Ghi qua CardStateManager
      try {
         const { CardStateManager } = await import("../../lib/CardStateManager");
         await CardStateManager.updateCardState(uid, cId, state);
      } catch (e) {
         // ignore
      }
    }
    if (Object.keys(mergedProfile).length > 0) {
      await set(`vibe_profile_${uid}`, mergedProfile);
    }

    // Đẩy Cloud (Dùng Batch)
    const batch = writeBatch(db);
    let batchCount = 0;
    
    for (const [dId, deck] of Object.entries(mergedDecks)) {
       const ref = doc(db, "vibe_decks", dId);
       batch.set(ref, removeUndefined(deck), { merge: true });
       batchCount++;
    }

    const pRef = doc(db, "users", uid);
    batch.set(pRef, removeUndefined(mergedProfile), { merge: true });
    batchCount++;

    const deckStatesToBatch: Record<string, Record<string, any>> = {};
    for (const [cId, state] of Object.entries(mergedCardStates)) {
       const s: any = state;
       const dId = s.deckId || "legacy_migrated_rescue";
       if (!deckStatesToBatch[dId]) deckStatesToBatch[dId] = {};
       deckStatesToBatch[dId][cId] = state;
    }
    
    for (const [dId, states] of Object.entries(deckStatesToBatch)) {
       const ref = doc(db, "users", uid, "vibe_deckStates", dId);
       batch.set(ref, removeUndefined({ states, deckId: dId, lastUpdatedAt: Date.now() }), { merge: true });
       batchCount++;
       if (batchCount >= 450) { // Firestore limit là 500
          await batch.commit();
          batchCount = 0;
       }
    }
    
    if (batchCount > 0) {
       await batch.commit();
    }

    log.push("Hoàn tất Force Merge! Tải lại trang để áp dụng.");
    return log.join('\n');
  } catch (error: any) {
    console.error("Force Merge Error", error);
    log.push("LỖI: " + error.message);
    return log.join('\n');
  }
}

export async function smartPushDeck(deckId: string): Promise<string> {
  const user = store.getCurrentUser() || auth.currentUser;
  if (!user) throw new Error("No authenticated user.");
  const uid = typeof user === 'string' ? user : (user as any).uid || (user as any).id;
  if (!uid) throw new Error("Could not determine user ID.");

  try {
    const { VibeSyncEngine } = await import("./VibeSyncEngine");
    const { CardStateManager } = await import("../../lib/CardStateManager");
    const { VibeProgressSyncManager } = await import("./VibeProgressSyncManager");
    const { setDoc } = await import("firebase/firestore");

    // 1. Get Deck's card IDs
    const deck = await VibeSyncEngine.getDeck(deckId);
    if (!deck || !deck.cards) return "Deck not found locally.";
    const cardIds = deck.cards.map((c: any) => c.id);

    // 2. Fetch local states
    const localCardStates: Record<string, any> = {};
    cardIds.forEach(cId => {
        const state = CardStateManager.getCardState(uid, cId);
        if (state) localCardStates[cId] = state;
    });

    // 3. Fetch cloud states
    let cloudCardStates: Record<string, any> = {};
    const deckStateRef = doc(db, "users", uid, "vibe_deckStates", deckId);
    const snap = await getDoc(deckStateRef);
    if (snap.exists()) {
        cloudCardStates = snap.data()?.states || {};
    }

    // 4. Merge LWW
    const mergedCardStates: Record<string, any> = {};
    for (const cId of cardIds) {
        const local = localCardStates[cId];
        const cloud = cloudCardStates[cId];
        
        if (local && cloud) {
            const localTime = local.updatedAt || local.lastUpdatedAt || 0;
            const cloudTime = cloud.updatedAt || cloud.lastUpdatedAt || 0;
            if (localTime === cloudTime) {
                const localM = local.mastery || 0;
                const cloudM = cloud.mastery || 0;
                mergedCardStates[cId] = localM > cloudM ? local : cloud;
            } else {
                mergedCardStates[cId] = localTime > cloudTime ? local : cloud;
            }
        } else {
            if (local || cloud) {
                mergedCardStates[cId] = local || cloud;
            }
        }
    }

    // 5. Save back to Local (without triggering queue)
    for (const [cId, state] of Object.entries(mergedCardStates)) {
        await CardStateManager.updateCardState(uid, cId, state);
    }

    // 6. Push to Cloud
    if (Object.keys(mergedCardStates).length > 0) {
        await setDoc(deckStateRef, removeUndefined({
            states: mergedCardStates,
            deckId: deckId,
            lastUpdatedAt: Date.now()
        }), { merge: true });
    }

    // 7. Push session progress
    await VibeProgressSyncManager.pushProgressToCloud(uid, deckId);

    // Try flushing the general sync queue as well
    await VibeSyncEngine.syncNow();

    return "OK";
  } catch (error: any) {
    console.error("Smart Push Deck Error", error);
    throw error;
  }
}

export async function smartPullDeck(deckId: string, forceBypassCache: boolean = false): Promise<string> {
  const user = store.getCurrentUser() || auth.currentUser;
  if (!user) throw new Error("No authenticated user.");
  const uid = typeof user === 'string' ? user : (user as any).uid || (user as any).id;
  if (!uid) throw new Error("Could not determine user ID.");

  try {
    const { VibeSyncEngine } = await import("./VibeSyncEngine");
    const { CardStateManager } = await import("../../lib/CardStateManager");
    const { getDoc, getDocFromServer } = await import("firebase/firestore");

    // 1. Get Deck's card IDs from local store
    const deck = await VibeSyncEngine.getDeck(deckId);
    if (!deck || !deck.cards) return "Deck not found locally.";
    const cardIds = deck.cards.map((c: any) => c.id);

    // 2. Fetch local states
    const localCardStates: Record<string, any> = {};
    cardIds.forEach((cId: string) => {
        const state = CardStateManager.getCardState(uid, cId);
        if (state) localCardStates[cId] = state;
    });

    // 3. Fetch cloud states (Selective: only 1 read)
    let cloudCardStates: Record<string, any> = {};
    const deckStateRef = doc(db, "users", uid, "vibe_deckStates", deckId);
    
    console.log(`[FIRESTORE READ] VibeSyncRescue: smartPullDeck on vibe_deckStates/${deckId}`);
    
    // Manual pull should bypass cache
    const snap = forceBypassCache ? await getDocFromServer(deckStateRef) : await getDoc(deckStateRef);
    
    if (snap.exists()) {
        cloudCardStates = snap.data()?.states || {};
    } else {
        return "No progress found on Cloud.";
    }

    // 4. Merge LWW (Last-Write-Wins)
    let updateCount = 0;
    for (const cId of cardIds) {
        const local = localCardStates[cId];
        const cloud = cloudCardStates[cId];
        
        let chosenState = null;
        if (local && cloud) {
            const localTime = local.updatedAt || local.lastUpdatedAt || 0;
            const cloudTime = cloud.updatedAt || cloud.lastUpdatedAt || 0;
            if (localTime === cloudTime) {
                const localM = local.mastery || 0;
                const cloudM = cloud.mastery || 0;
                chosenState = localM > cloudM ? local : cloud;
            } else {
                chosenState = localTime > cloudTime ? local : cloud;
            }
        } else {
            chosenState = local || cloud;
        }

        // 5. Update local state reactively via CardStateManager
        if (chosenState && (!local || JSON.stringify(local) !== JSON.stringify(chosenState))) {
            await CardStateManager.updateCardState(uid, cId, chosenState);
            updateCount++;
        }
    }

    return `Synced ${updateCount} updates.`;
  } catch (error: any) {
    console.error("Smart Pull Deck Error", error);
    throw error;
  }
}
