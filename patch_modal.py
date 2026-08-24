import sys

with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "r") as f:
    content = f.read()

# Import smartPullDeck
if "smartPullDeck" not in content:
    content = content.replace("import { VibeSyncEngine } from './sync/VibeSyncEngine';", "import { VibeSyncEngine } from './sync/VibeSyncEngine';\nimport { smartPullDeck } from './sync/VibeSyncRescue';")

# Add pull state
if "isAutoPulling" not in content:
    content = content.replace("const [lastBackup, setLastBackup] = useState<BackupData | null>(null);", "const [lastBackup, setLastBackup] = useState<BackupData | null>(null);\n  const [isAutoPulling, setIsAutoPulling] = useState(false);\n  const [pullStatus, setPullStatus] = useState<'idle'|'syncing'|'success'|'error'>('idle');")

# Add useEffect for pulling
useEffect_pull = """
  useEffect(() => {
    if (isOpen && deck) {
      setIsAutoPulling(true);
      setPullStatus('syncing');
      smartPullDeck(deck.id, false)
        .then(() => {
          setPullStatus('success');
        })
        .catch((err) => {
          console.error("Auto pull failed", err);
          setPullStatus('error');
        })
        .finally(() => {
          setIsAutoPulling(false);
          // Optional: clear success message after some time
          setTimeout(() => setPullStatus('idle'), 3000);
        });
    }
  }, [isOpen, deck]);
"""

if "smartPullDeck(deck.id, false)" not in content:
    content = content.replace("const weakCardIds = useMemo(() => {", useEffect_pull + "\n  const weakCardIds = useMemo(() => {")

# Add UI for pulling status
status_ui = """
                <div className="flex items-center gap-1.5 mt-1 opacity-70">
                  {pullStatus === 'syncing' && (
                    <>
                      <RefreshCw className="w-3 h-3 animate-spin text-zinc-500" />
                      <span className="text-[11px] font-medium text-zinc-500">Đang đồng bộ...</span>
                    </>
                  )}
                  {pullStatus === 'success' && (
                    <>
                      <span className="text-[11px] font-medium text-green-600 dark:text-green-400">Dữ liệu mới nhất</span>
                    </>
                  )}
                  {pullStatus === 'error' && (
                    <>
                      <AlertTriangle className="w-3 h-3 text-red-500" />
                      <span className="text-[11px] font-medium text-red-500">Đồng bộ thất bại</span>
                    </>
                  )}
                </div>
"""

content = content.replace("</span>\n                  {weakCardIds.length > 0 && (", "</span>\n                  {weakCardIds.length > 0 && (\n" + "                    <span className=\"font-semibold text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-500/10 px-2 py-0.5 rounded-md\">\n                      {weakCardIds.length} thẻ X\n                    </span>\n                  )}\n" + status_ui + "\n                </p>\n")

# Need to be careful with replace, let's just insert it cleanly.
with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "w") as f:
    f.write(content)
print("Patched Modal roughly, let's refine.")
