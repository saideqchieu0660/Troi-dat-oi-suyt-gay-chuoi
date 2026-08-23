import sys
with open("src/components/DeckList.tsx", "r") as f:
    content = f.read()

old_code = """                      {onCategoryReviewHardCards && (() => {
                         const remindIds = JSON.parse(localStorage.getItem("remind_later_items") || "[]");
                         const hardCardsInCat = subjectDecks.flatMap(d => d.cards || []).filter(c => c.isHard === true || remindIds.includes(c.id));
                         const uniqueHardCards = Array.from(new Map(hardCardsInCat.map(c => [c.id, c])).values());
                          
                         return (
                           <button
                             onClick={() => uniqueHardCards.length > 0 && onCategoryReviewHardCards(subject, subjectDecks)}
                             disabled={uniqueHardCards.length === 0}
                             className={cn(
                               "mr-1 text-xs font-black text-white px-4 py-2.5 rounded-xl transition-all flex items-center gap-1.5 focus:outline-none shrink-0",
                               uniqueHardCards.length > 0
                                 ? "bg-gradient-to-r from-red-500 to-rose-500 hover:from-red-600 hover:to-rose-600 hover:scale-105 active:scale-95 shadow-[0_0_15px_rgba(239,68,68,0.4)] cursor-pointer"
                                 : "bg-red-300 dark:bg-red-900/50 opacity-50 cursor-not-allowed"
                             )}
                             title={uniqueHardCards.length > 0 ? `Ôn lại ${uniqueHardCards.length} thẻ khó trong mục này` : `Không có thẻ nào bị đánh dấu X trong mục này`}
                           >
                             <span className="flex items-center justify-center bg-white/20 rounded-full w-5 h-5 text-[10px]">{uniqueHardCards.length}</span>
                             <span className="hidden leading-none sm:inline">Ôn Thẻ X</span>
                             <span className="sm:hidden leading-none">Thẻ X</span>
                           </button>
                         );
                      })()}"""

new_code = """                      {onCategoryReviewHardCards && (() => {
                         const hardCount = subjectDecks.reduce((acc, d) => acc + (d.vibe_weak_count || 0), 0);
                          
                         return (
                           <button
                             onClick={() => hardCount > 0 && onCategoryReviewHardCards(subject, subjectDecks)}
                             disabled={hardCount === 0}
                             className={cn(
                               "mr-1 text-xs font-black text-white px-4 py-2.5 rounded-xl transition-all flex items-center gap-1.5 focus:outline-none shrink-0",
                               hardCount > 0
                                 ? "bg-gradient-to-r from-red-500 to-rose-500 hover:from-red-600 hover:to-rose-600 hover:scale-105 active:scale-95 shadow-[0_0_15px_rgba(239,68,68,0.4)] cursor-pointer"
                                 : "bg-red-300 dark:bg-red-900/50 opacity-50 cursor-not-allowed"
                             )}
                             title={hardCount > 0 ? `Ôn lại ${hardCount} thẻ khó trong mục này` : `Không có thẻ nào bị đánh dấu X trong mục này`}
                           >
                             <span className="flex items-center justify-center bg-white/20 rounded-full w-5 h-5 text-[10px]">{hardCount}</span>
                             <span className="hidden leading-none sm:inline">Ôn Thẻ X</span>
                             <span className="sm:hidden leading-none">Thẻ X</span>
                           </button>
                         );
                      })()}"""
content = content.replace(old_code, new_code)

old_code2 = """                    {onCategoryReviewHardCards && (() => {
                       const remindIds = JSON.parse(localStorage.getItem("remind_later_items") || "[]");
                       const hardCardsInCat = subjectDecks.flatMap(d => d.cards || []).filter(c => c.isHard === true || remindIds.includes(c.id));
                       const uniqueHardCards = Array.from(new Map(hardCardsInCat.map(c => [c.id, c])).values());
                       
                       return (
                         <button
                           onClick={(e) => {
                             e.stopPropagation();
                             if (uniqueHardCards.length > 0) onCategoryReviewHardCards(subject, subjectDecks);
                           }}
                           disabled={uniqueHardCards.length === 0}
                           className={cn(
                             "text-[10px] sm:text-xs font-black text-white px-2 sm:px-3 py-1.5 sm:py-2 rounded-xl transition-all flex items-center gap-1.5 shrink-0",
                             uniqueHardCards.length > 0
                               ? "bg-gradient-to-r from-red-400 to-rose-500 hover:from-red-500 hover:to-rose-600 hover:scale-105 shadow-md cursor-pointer"
                               : "bg-red-300 dark:bg-red-900/50 opacity-50 cursor-not-allowed"
                           )}
                           title={`Ôn ${uniqueHardCards.length} thẻ khó`}
                         >
                           <span className="flex items-center justify-center bg-white/20 rounded-full w-4 h-4 text-[9px]">{uniqueHardCards.length}</span>
                           <span className="hidden sm:inline">Ôn Thẻ X</span>
                         </button>
                       );
                    })()}"""

new_code2 = """                    {onCategoryReviewHardCards && (() => {
                       const hardCount = subjectDecks.reduce((acc, d) => acc + (d.vibe_weak_count || 0), 0);
                       
                       return (
                         <button
                           onClick={(e) => {
                             e.stopPropagation();
                             if (hardCount > 0) onCategoryReviewHardCards(subject, subjectDecks);
                           }}
                           disabled={hardCount === 0}
                           className={cn(
                             "text-[10px] sm:text-xs font-black text-white px-2 sm:px-3 py-1.5 sm:py-2 rounded-xl transition-all flex items-center gap-1.5 shrink-0",
                             hardCount > 0
                               ? "bg-gradient-to-r from-red-400 to-rose-500 hover:from-red-500 hover:to-rose-600 hover:scale-105 shadow-md cursor-pointer"
                               : "bg-red-300 dark:bg-red-900/50 opacity-50 cursor-not-allowed"
                           )}
                           title={`Ôn ${hardCount} thẻ khó`}
                         >
                           <span className="flex items-center justify-center bg-white/20 rounded-full w-4 h-4 text-[9px]">{hardCount}</span>
                           <span className="hidden sm:inline">Ôn Thẻ X</span>
                         </button>
                       );
                    })()}"""
content = content.replace(old_code2, new_code2)

old_code3 = """                    {subjectDecks.map((deck, idx) => {
                      const masteredCount = deck.cards.filter(c => c.mastery >= 80).length;
                      const masteryRate = deck.cards.length > 0 ? Math.round((masteredCount / deck.cards.length) * 100) : 0;
                      
                      const estimatedSeconds = deck.cards.reduce((acc, card) => {
                          const m = card.mastery || 0;
                          if (m >= 80) return acc + 10;
                          if (m >= 50) return acc + 25;
                          if (m >= 20) return acc + 40;
                          return acc + 60;
                      }, 0);
                      const estimatedMinutes = Math.ceil(estimatedSeconds / 60);
                      
                      const isOfflineUnavailable = !isOnline && !offlineDeckIds.has(deck.id);"""

new_code3 = """                    {subjectDecks.map((deck, idx) => {
                      const masteredCount = deck.vibe_mastered_count ?? deck.cards.filter(c => c.mastery >= 80).length;
                      const masteryRate = deck.cards.length > 0 ? Math.round((masteredCount / deck.cards.length) * 100) : 0;
                      
                      const estimatedSeconds = deck.vibe_estimated_seconds ?? deck.cards.reduce((acc, card) => {
                          const m = card.mastery || 0;
                          if (m >= 80) return acc + 10;
                          if (m >= 50) return acc + 25;
                          if (m >= 20) return acc + 40;
                          return acc + 60;
                      }, 0);
                      const estimatedMinutes = Math.ceil(estimatedSeconds / 60);
                      
                      const isOfflineUnavailable = !isOnline && !offlineDeckIds.has(deck.id);"""
content = content.replace(old_code3, new_code3)

with open("src/components/DeckList.tsx", "w") as f:
    f.write(content)
