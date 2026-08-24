import sys

with open("src/components/DeckOptionsMenu.tsx", "r") as f:
    content = f.read()

# Add RefreshCw to lucide imports
content = content.replace("CloudUpload } from 'lucide-react';", "CloudUpload, RefreshCw } from 'lucide-react';")

# Add smartPullDeck import
if "smartPullDeck" not in content:
    content = content.replace("import { VibeProgressSyncManager }", "import { smartPullDeck } from '../vibe-sandbox/sync/VibeSyncRescue';\nimport { VibeProgressSyncManager }")

# Add state for pull
if "isPulling" not in content:
    content = content.replace("const [pinnedDecks, setPinnedDecks] = useState<string[]>([]);", "const [pinnedDecks, setPinnedDecks] = useState<string[]>([]);\n  const [isPulling, setIsPulling] = useState(false);")

# Add handlePull method
handle_pull = """
  const handlePull = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setShowDeckMenu(false);
    setIsPulling(true);
    try {
      await smartPullDeck(deck.id, true);
      toast.success("Đã đồng bộ tiến trình thành công!");
    } catch (err: any) {
      toast.error(err.message || "Lỗi khi đồng bộ tiến trình.");
    } finally {
      setIsPulling(false);
    }
  };
"""

content = content.replace("const handleDownloadOffline = async", handle_pull + "\n  const handleDownloadOffline = async")

# Add the button
pull_button = """
            <button
              onClick={handlePull}
              disabled={isPulling}
              className="w-full flex items-center gap-3 px-4 py-3 text-sm text-left hover:bg-zinc-100 dark:hover:bg-zinc-800 text-zinc-900 dark:text-zinc-100 transition-colors cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isPulling ? "animate-spin" : ""}`} />
              Đồng bộ thủ công
            </button>
"""

content = content.replace("<div className=\"w-full h-px bg-zinc-200 dark:bg-zinc-800 my-1\"></div>", pull_button + "\n            <div className=\"w-full h-px bg-zinc-200 dark:bg-zinc-800 my-1\"></div>")

with open("src/components/DeckOptionsMenu.tsx", "w") as f:
    f.write(content)
print("Patched DeckOptionsMenu!")
