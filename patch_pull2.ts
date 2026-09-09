import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/sync/VibeSyncEngine.ts', 'utf8');

content = content.replace(
  "let updatedCardsCount = 0;",
  "let updatedCardsCount = 0;\n      const pulledStates: any[] = [];"
);

content = content.replace(
  "updatedCardsCount++;",
  `updatedCardsCount++;
                      pulledStates.push({
                          cardId,
                          mastery: statePayload.mastery,
                          isWeakCard: typeof statePayload.isWeakCard === "boolean" ? statePayload.isWeakCard : statePayload.isHard,
                          nextReviewDate: statePayload.nextReviewDate,
                          updatedAt: serverPullTime
                      });`
);

content = content.replace(
  `window.dispatchEvent(new CustomEvent('vibe-card-states-pulled', { detail: { count: updatedCardsCount } }));`,
  `window.dispatchEvent(new CustomEvent('vibe-card-states-pulled', { detail: { count: updatedCardsCount } }));
            window.dispatchEvent(new CustomEvent('vibe-card-states-updated', { detail: { states: pulledStates } }));`
);

writeFileSync('src/vibe-sandbox/sync/VibeSyncEngine.ts', content);
console.log("Patched successfully");
