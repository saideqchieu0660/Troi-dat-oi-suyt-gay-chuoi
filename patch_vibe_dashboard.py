import sys
with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    content = f.read()

old_code = """          if (savedState) {
            const cardTs = getCardTimestamp(card);
            const savedTs = getCardTimestamp(savedState);
            
            if (savedTs >= cardTs) {
              return {
                ...card,
                mastery:
                  typeof savedState.mastery === "number" &&
                  !isNaN(savedState.mastery)
                    ? savedState.mastery
                    : Number(card.mastery) || 0,
                nextReviewDate:
                  typeof savedState.nextReviewDate === "number"
                    ? savedState.nextReviewDate
                    : card.nextReviewDate,
                nextReview:
                  typeof savedState.nextReview === "number"
                    ? savedState.nextReview
                    : card.nextReview,
                interval:
                  typeof savedState.interval === "number"
                    ? savedState.interval
                    : card.interval,
                repetitionCount:
                  typeof savedState.repetitionCount === "number"
                    ? savedState.repetitionCount
                    : card.repetitionCount,
                easeFactor:
                  typeof savedState.easeFactor === "number"
                    ? savedState.easeFactor
                    : card.easeFactor,
                isNewCard:
                  typeof savedState.isNewCard === "boolean"
                    ? savedState.isNewCard
                    : false,
                isHard:
                  typeof savedState.isWeakCard !== "undefined"
                    ? savedState.isWeakCard
                    : card.isHard,
                updatedAt: savedState.updatedAt || card.updatedAt
              };
            }
          }
          return card;
        });
      }
      return clonedDeck;
    });
  }, [rawDecks, personalCardStates]);"""

new_code = """          if (savedState) {
            const cardTs = getCardTimestamp(card);
            const savedTs = getCardTimestamp(savedState);
            
            if (savedTs >= cardTs) {
              return {
                ...card,
                mastery:
                  typeof savedState.mastery === "number" &&
                  !isNaN(savedState.mastery)
                    ? savedState.mastery
                    : Number(card.mastery) || 0,
                nextReviewDate:
                  typeof savedState.nextReviewDate === "number"
                    ? savedState.nextReviewDate
                    : card.nextReviewDate,
                nextReview:
                  typeof savedState.nextReview === "number"
                    ? savedState.nextReview
                    : card.nextReview,
                interval:
                  typeof savedState.interval === "number"
                    ? savedState.interval
                    : card.interval,
                repetitionCount:
                  typeof savedState.repetitionCount === "number"
                    ? savedState.repetitionCount
                    : card.repetitionCount,
                easeFactor:
                  typeof savedState.easeFactor === "number"
                    ? savedState.easeFactor
                    : card.easeFactor,
                isNewCard:
                  typeof savedState.isNewCard === "boolean"
                    ? savedState.isNewCard
                    : false,
                isHard:
                  typeof savedState.isWeakCard !== "undefined"
                    ? savedState.isWeakCard
                    : card.isHard,
                updatedAt: savedState.updatedAt || card.updatedAt
              };
            }
          }
          return card;
        });
        
        let weakCount = 0;
        let masteredCount = 0;
        let estimatedSecs = 0;
        
        const remindIds = JSON.parse(localStorage.getItem("remind_later_items") || "[]");

        clonedDeck.cards.forEach((c: any) => {
           if (c.isHard || remindIds.includes(c.id)) weakCount++;
           const m = c.mastery || 0;
           if (m >= 80) { masteredCount++; estimatedSecs += 10; }
           else if (m >= 50) { estimatedSecs += 25; }
           else if (m >= 20) { estimatedSecs += 40; }
           else { estimatedSecs += 60; }
        });
        clonedDeck.vibe_weak_count = weakCount;
        clonedDeck.vibe_mastered_count = masteredCount;
        clonedDeck.vibe_estimated_seconds = estimatedSecs;
      }
      return clonedDeck;
    });
  }, [rawDecks, personalCardStates]);"""

content = content.replace(old_code, new_code)
with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.write(content)
