import os

filepath = "src/pages/TeacherDashboard.tsx"
with open(filepath, "r") as f:
    content = f.read()

# Add hiddenCategories state
import_lucide = '  Trash2,\n  Eye,\n  EyeOff,\n  ChevronLeft,'
if '  EyeOff,\n' not in content:
    content = content.replace('  Trash2,\n  ChevronLeft,', import_lucide)

state_str = '  const [hiddenCategories, setHiddenCategories] = useState<string[]>([]);\n  const [showMoveBulkModal'
if 'const [hiddenCategories, setHiddenCategories]' not in content:
    content = content.replace('  const [showMoveBulkModal', state_str)

# Add fetch for hiddenCategories
fetch_hidden = """        if (!isMounted) return;
        const { query, where, limit } = await import("firebase/firestore");
        
        try {
          const { doc, getDoc } = await import("firebase/firestore");
          const hiddenRef = doc(db, "vibe_settings", "dashboard_config");
          const hiddenSnap = await getDoc(hiddenRef);
          if (hiddenSnap.exists() && isMounted) {
            setHiddenCategories(hiddenSnap.data().hiddenCategories || []);
          }
        } catch (e) { console.error("Failed to fetch hidden categories", e); }
"""
if 'const hiddenRef = doc(db, "vibe_settings", "dashboard_config");' not in content:
    content = content.replace(
        '        if (!isMounted) return;\n        const { query, where, limit } = await import("firebase/firestore");',
        fetch_hidden
    )

# Add toggle function
toggle_func = """
  const toggleCategoryVisibility = async (subject: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const { db } = await import("../lib/firebase");
      const { doc, getDoc, setDoc } = await import("firebase/firestore");
      const hiddenRef = doc(db, "vibe_settings", "dashboard_config");
      const hiddenSnap = await getDoc(hiddenRef);
      let currentHidden: string[] = [];
      if (hiddenSnap.exists()) {
        currentHidden = hiddenSnap.data().hiddenCategories || [];
      }
      const isHidden = currentHidden.includes(subject);
      if (isHidden) {
        currentHidden = currentHidden.filter(c => c !== subject);
      } else {
        currentHidden.push(subject);
      }
      await setDoc(hiddenRef, { hiddenCategories: currentHidden }, { merge: true });
      setHiddenCategories(currentHidden);
      toast(isHidden ? `Đã hiện phân mục "${subject}" cho học viên.` : `Đã ẩn phân mục "${subject}" đối với học viên.`);
    } catch (err: any) {
      toast("Lỗi khi thay đổi trạng thái phân mục: " + err.message);
    }
  };

  const handleRenameCategory = async (oldName: string, newName: string) => {"""

if 'const toggleCategoryVisibility =' not in content:
    content = content.replace('  const handleRenameCategory = async (oldName: string, newName: string) => {', toggle_func)


# Add UI icon
ui_icon = """                                      <h4 className="text-xs font-black uppercase tracking-widest text-orange-600 dark:text-orange-500 flex items-center gap-1.5">
                                        📂 {subject}{" "}
                                        <span className="opacity-60 text-[10px] font-bold font-mono">
                                          ({subjectDecks.length} bộ)
                                        </span>
                                      </h4>
                                      <button
                                        type="button"
                                        title={hiddenCategories.includes(subject) ? "Đang ẩn với học viên. Nhấn để hiện." : "Đang hiện với học viên. Nhấn để ẩn."}
                                        onClick={(e) => toggleCategoryVisibility(subject, e)}
                                        className={`ml-2 p-1.5 rounded-full transition-colors border-none cursor-pointer flex items-center justify-center ${hiddenCategories.includes(subject) ? 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-950 dark:text-red-400' : 'bg-emerald-100 text-emerald-600 hover:bg-emerald-200 dark:bg-emerald-950 dark:text-emerald-400'}`}
                                      >
                                        {hiddenCategories.includes(subject) ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                      </button>"""

if '<EyeOff className=' not in content:
    content = content.replace('''                                      <h4 className="text-xs font-black uppercase tracking-widest text-orange-600 dark:text-orange-500 flex items-center gap-1.5">
                                        📂 {subject}{" "}
                                        <span className="opacity-60 text-[10px] font-bold font-mono">
                                          ({subjectDecks.length} bộ)
                                        </span>
                                      </h4>''', ui_icon)

with open(filepath, "w") as f:
    f.write(content)
print("Patched!")
