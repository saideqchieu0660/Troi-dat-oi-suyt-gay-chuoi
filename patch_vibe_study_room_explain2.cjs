const fs = require('fs');
const file = 'src/vibe-sandbox/VibeStudyRoom.tsx';
let content = fs.readFileSync(file, 'utf8');

const targetStr2 = `
        if (!res2.ok) {
           throw new Error(await res2.text());
        }
        const text = await res2.text();
        data = JSON.parse(text);
      }

      setDeepExplanation({
        text: data.result,
        cardId: currentCard.id,
        originalFront: currentCard.front || "",
        originalBack: currentCard.back || "",
        originalExample: currentCard.example_sentence || ""
      });
`;

const replaceStr2 = `
        if (!res2.ok) {
           throw new Error(await res2.text());
        }
        let accumulated = "";
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
      }
`;

content = content.replace(targetStr2, replaceStr2);

fs.writeFileSync(file, content);
