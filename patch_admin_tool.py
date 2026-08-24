import sys

with open("src/vibe-sandbox/VibeAdminProgressTool.tsx", "r") as f:
    content = f.read()

content = content.replace('import { Download, Upload, AlertTriangle, ShieldAlert } from "lucide-react";', 'import { Download, Upload, AlertTriangle, ShieldAlert, ChevronDown, ChevronRight } from "lucide-react";')

old_state = """export function VibeAdminProgressTool() {
  const [decks, setDecks] = useState<any[]>([]);
  const [selectedDeckId, setSelectedDeckId] = useState<string>("");
  const [isExporting, setIsExporting] = useState(false);"""
new_state = """export function VibeAdminProgressTool() {
  const [decks, setDecks] = useState<any[]>([]);
  const [selectedDeckId, setSelectedDeckId] = useState<string>("");
  const [expandedSubject, setExpandedSubject] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState(false);"""
content = content.replace(old_state, new_state)

old_grouped = """  const user = store.getCurrentUser();

  useEffect(() => {"""
new_grouped = """  const user = store.getCurrentUser();

  const groupedDecks = decks.reduce((acc, deck) => {
    const subject = deck.subject || "Uncategorized";
    if (!acc[subject]) acc[subject] = [];
    acc[subject].push(deck);
    return acc;
  }, {} as Record<string, any[]>);

  useEffect(() => {"""
content = content.replace(old_grouped, new_grouped)

old_select = """        <div>
          <label className="block text-sm font-bold mb-2">Target Deck</label>
          <select 
            className="w-full bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-3"
            value={selectedDeckId}
            onChange={(e) => {
              setSelectedDeckId(e.target.value);
              setError("");
              setSuccess("");
            }}
          >
            <option value="">-- Select a Deck --</option>
            {decks.map(d => (
              <option key={d.id} value={d.id}>{d.title} ({d.subject}) - {d.id}</option>
            ))}
          </select>
        </div>"""
new_select = """        <div>
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
        </div>"""
content = content.replace(old_select, new_select)

with open("src/vibe-sandbox/VibeAdminProgressTool.tsx", "w") as f:
    f.write(content)

print("Patched!")
