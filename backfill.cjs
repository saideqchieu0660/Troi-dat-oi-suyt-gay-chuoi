const admin = require('firebase-admin');
const serviceAccount = require('./firebase-applet-config.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
async function run() {
  const db = admin.firestore();
  const snap = await db.collection('vibe_decks').get();
  let count = 0;
  for (const doc of snap.docs) {
    if (doc.data().vibe_visibility === undefined) {
      await doc.ref.update({ vibe_visibility: 'public' });
      count++;
    }
  }
  console.log('Backfilled ' + count + ' decks');
}
run().catch(console.error);
