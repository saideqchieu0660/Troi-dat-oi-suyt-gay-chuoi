const fs = require('fs');
const file = 'src/vibe-sandbox/VibeStudyRoom.tsx';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(/const text = await res2\.text\(\);\s*data = JSON\.parse\(text\);\s*\}\s*setDeepExplanation\(\{\s*text: data\.result,\s*cardId: currentCard\.id,\s*originalFront: currentCard\.front \|\| "",\s*originalBack: currentCard\.back \|\| "",\s*originalExample: currentCard\.example_sentence \|\| ""\s*\}\);/,
`        let accumulated = "";
        setDeepExplanation({
          text: accumulated,
          cardId: currentCard.id,
          originalFront: currentCard.front || "",
          originalBack: currentCard.back || "",
          originalExample: currentCard.example_sentence || ""
        });
        await processStream(res2, (chunk) => {
           accumulated += chunk;
           setDeepExplanation({
              text: accumulated,
              cardId: currentCard.id,
              originalFront: currentCard.front || "",
              originalBack: currentCard.back || "",
              originalExample: currentCard.example_sentence || ""
           });
        });
      }`);

fs.writeFileSync(file, content);
