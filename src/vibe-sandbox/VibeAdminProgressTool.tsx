import { useState, useEffect } from "react";
import { Download, Upload, AlertTriangle, ShieldAlert, ChevronDown, ChevronRight } from "lucide-react";
import { store } from "../lib/store";
import { VibeSyncEngine } from "./sync/VibeSyncEngine";
import { CardStateManager } from "../lib/CardStateManager";

export function VibeAdminProgressTool() {
  const [decks, setDecks] = useState<any[]>([]);
  const [selectedDeckId, setSelectedDeckId] = useState<string>("");
  const [expandedSubject, setExpandedSubject] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [fileToImport, setFileToImport] = useState<File | null>(null);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");
  
  const user = store.getCurrentUser();

  const groupedDecks = decks.reduce((acc, deck) => {
    const subject = deck.subject || "Uncategorized";
    if (!acc[subject]) acc[subject] = [];
    acc[subject].push(deck);
    return acc;
  }, {} as Record<string, any[]>);

  useEffect(() => {
    // Load local decks
    VibeSyncEngine.getLocalDecks().then(localDecks => {
      setDecks(localDecks);
    });
  }, []);

  const handleExport = async () => {
    if (!selectedDeckId || !user) return;
    setIsExporting(true);
    setError("");
    setSuccess("");
    try {
      // 1. Ensure states are hydrated
      await CardStateManager.hydrateStates(user.id);
      
      // 2. Fetch the deck to know which cards belong to it
      const deck = await VibeSyncEngine.getDeck(selectedDeckId);
      if (!deck || !deck.cards) {
        throw new Error("Deck not found or has no cards");
      }
      
      const cardIds = deck.cards.map(c => c.id);
      const exportedCards: any[] = [];
      
      cardIds.forEach(cardId => {
        const state = CardStateManager.getCardState(user.id, cardId);
        if (state) {
          exportedCards.push({
            card_id: state.cardId,
            mastery: state.mastery,
            isHard: state.isHard,
            repetitionCount: state.repetitionCount,
            interval: state.interval,
            easeFactor: state.easeFactor,
            nextReviewDate: state.nextReviewDate,
            lastPointAwarded: state.lastPointAwarded,
            updated_at: state.updatedAt
          });
        }
      });
      
      const exportPayload = {
        deck_id: selectedDeckId,
        exported_at: new Date().toISOString(),
        cards: exportedCards
      };
      
      const blob = new Blob([JSON.stringify(exportPayload, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `deck_progress_${selectedDeckId}_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setSuccess(`Exported ${exportedCards.length} card states successfully.`);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to export");
    } finally {
      setIsExporting(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFileToImport(e.target.files[0]);
    }
  };

  const handleImport = async () => {
    if (!selectedDeckId || !user || !fileToImport) return;
    
    const confirmMsg = "This will permanently overwrite current progress locally and on the server. Proceed?";
    if (!window.confirm(confirmMsg)) return;
    
    setIsImporting(true);
    setError("");
    setSuccess("");
    
    try {
      const text = await fileToImport.text();
      const payload = JSON.parse(text);
      
      if (!payload.deck_id || !payload.cards || !Array.isArray(payload.cards)) {
        throw new Error("Invalid JSON format. Expected deck_id and cards array.");
      }
      
      if (payload.deck_id !== selectedDeckId) {
        throw new Error(`JSON deck_id (${payload.deck_id}) does not match selected deck (${selectedDeckId})`);
      }
      
      // 1. Send to server for bulk overwrite
      const idToken = await (user as any).getIdToken?.();
      // If we don't have getIdToken on user (if user is just local), we can try to get it from firebase auth
      const { auth } = await import("../lib/firebase");
      const currentFbUser = auth.currentUser;
      const token = currentFbUser ? await currentFbUser.getIdToken() : "";
      
      if (!token) {
         throw new Error("Cannot authorize request. Please sign in again.");
      }

      const res = await fetch(`/api/admin/decks/${selectedDeckId}/bulk-overwrite`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ cards: payload.cards })
      });
      
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.error || "Server bulk overwrite failed");
      }
      
      const responseData = await res.json();
      
      // 2. Overwrite local IDB state via CardStateManager
      await CardStateManager.hydrateStates(user.id);
      
      // First, wipe all existing progress for the cards in this deck
      const deck = await VibeSyncEngine.getDeck(selectedDeckId);
      if (deck && deck.cards) {
        for (const c of deck.cards) {
           await CardStateManager.updateCardState(user.id, c.id, {
              mastery: 0,
              isHard: false,
              repetitionCount: 0,
              interval: 0,
              easeFactor: 2.5,
              nextReviewDate: 0,
              lastPointAwarded: 0,
              updatedAt: responseData.serverTime || Date.now()
           });
        }
      }
      
      // Then, apply the imported payload
      for (const card of payload.cards) {
        if (!card.card_id) continue;
        const patch = {
          mastery: card.mastery || 0,
          isHard: card.isHard || false,
          repetitionCount: card.repetitionCount || 0,
          interval: card.interval || 0,
          easeFactor: card.easeFactor || 2.5,
          nextReviewDate: card.nextReviewDate || 0,
          lastPointAwarded: card.lastPointAwarded || 0,
          updatedAt: responseData.serverTime || Date.now()
        };
        // This updates IDB and memory, and triggers UI re-renders
        await CardStateManager.updateCardState(user.id, card.card_id, patch);
      }
      
      setSuccess(`Imported and overwritten ${payload.cards.length} card states successfully.`);
      setFileToImport(null);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to import");
    } finally {
      setIsImporting(false);
    }
  };

  if (!user || (user.role !== "admin" && user.role !== "Admin" && user.role !== "teacher")) {
    return null; // Safety check
  }

  return (
    <div className="glass p-6 rounded-3xl border border-red-500/30 w-full overflow-hidden animate-in fade-in slide-in-from-top-4 space-y-6 mt-8">
      <div className="flex items-center gap-3 border-b border-red-500/20 pb-4">
        <ShieldAlert className="w-6 h-6 text-red-500" />
        <div>
          <h2 className="text-xl font-bold text-red-600 dark:text-red-400">Data Sync Tools (Admin)</h2>
          <p className="text-sm opacity-80">Export or Bulk-Overwrite deck progress for the current user.</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-bold mb-2">Target Deck</label>
          <div className="w-full bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden">
            {Object.entries(groupedDecks).length === 0 ? (
              <div className="p-4 text-sm opacity-50 text-center">No decks available</div>
            ) : (
              Object.entries(groupedDecks).map(([subject, subjectDecks]: [string, any]) => (
                <div key={subject} className="border-b border-zinc-200 dark:border-zinc-800 last:border-0">
                  <button
                    onClick={() => setExpandedSubject(expandedSubject === subject ? null : subject)}
                    className="w-full flex items-center justify-between p-4 text-left hover:bg-zinc-200/50 dark:hover:bg-zinc-800/50 transition-colors"
                  >
                    <div className="flex items-center gap-2 font-bold">
                      {expandedSubject === subject ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                      {subject}
                    </div>
                    <span className="text-xs bg-zinc-200 dark:bg-zinc-800 px-2 py-1 rounded-full">{subjectDecks.length}</span>
                  </button>
                  {expandedSubject === subject && (
                    <div className="p-2 bg-white/50 dark:bg-black/20 flex flex-col gap-1">
                      {subjectDecks.map((d: any) => (
                        <button
                          key={d.id}
                          onClick={() => {
                            setSelectedDeckId(d.id);
                            setError("");
                            setSuccess("");
                          }}
                          className={`text-left p-3 rounded-lg transition-colors text-sm ${
                            selectedDeckId === d.id 
                              ? "bg-red-500/10 text-red-600 dark:text-red-400 font-bold border border-red-500/20" 
                              : "hover:bg-zinc-200 dark:hover:bg-zinc-800 opacity-80"
                          }`}
                        >
                          {d.title} <span className="opacity-50 text-xs ml-2">({d.id})</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {selectedDeckId && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            {/* Export Panel */}
            <div className="p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-black/50 space-y-4">
              <h3 className="font-bold text-sm flex items-center gap-2">
                <Download className="w-4 h-4" /> Export Progress
              </h3>
              <p className="text-xs opacity-70">
                Downloads the current progress state (mastery, spaced-repetition intervals) of all cards in this deck as a JSON file.
              </p>
              <button 
                onClick={handleExport}
                disabled={isExporting}
                className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold disabled:opacity-50 transition-colors"
              >
                {isExporting ? "Exporting..." : "Export Deck Progress (JSON)"}
              </button>
            </div>

            {/* Import Panel */}
            <div className="p-4 rounded-xl border border-red-500/30 bg-red-500/5 space-y-4">
              <h3 className="font-bold text-sm flex items-center gap-2 text-red-600 dark:text-red-400">
                <Upload className="w-4 h-4" /> Import & Overwrite
              </h3>
              <p className="text-xs opacity-70">
                Upload a previously exported JSON file to completely overwrite the progress on this device and bulk-sync to the server.
              </p>
              <input 
                type="file" 
                accept=".json" 
                onChange={handleFileChange}
                className="block w-full text-sm text-zinc-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100"
              />
              <button 
                onClick={handleImport}
                disabled={isImporting || !fileToImport}
                className="w-full py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-bold disabled:opacity-50 transition-colors"
              >
                {isImporting ? "Importing..." : "Import & Overwrite Progress"}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 rounded-lg flex items-center gap-2 text-sm mt-4">
            <AlertTriangle className="w-4 h-4" /> {error}
          </div>
        )}
        
        {success && (
          <div className="p-3 bg-green-500/10 border border-green-500/20 text-green-600 dark:text-green-400 rounded-lg text-sm mt-4">
            {success}
          </div>
        )}
      </div>
    </div>
  );
}
