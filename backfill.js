import { readFileSync } from 'fs';
import admin from 'firebase-admin';

const serviceAccount = JSON.parse(readFileSync('./firebase-applet-config.json', 'utf8'));
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

async function run() {
  const db = admin.firestore();
  const snap = await db.collection('vibe_decks').get();
  let count = 0;
  const batch = db.batch();
  
  for (const doc of snap.docs) {
    const data = doc.data();
    if (data.vibe_isHidden === undefined) {
      batch.update(doc.ref, { vibe_isHidden: false });
      count++;
    }
  }
  
  if (count > 0) {
    await batch.commit();
  }
  console.log('Backfilled ' + count + ' decks');
}

run().catch(console.error);
