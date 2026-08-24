import sys

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    content = f.read()

notebook_tab_content = """      {activeTab === "notebook" && (
        <div className="w-full">
          <motion.div
            key="notebook-tab"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="w-full max-w-4xl mx-auto"
          >
            <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-6 shadow-xl flex flex-col min-h-[70vh]">
              <div className="flex items-center justify-between mb-8 pb-4 border-b border-zinc-100 dark:border-zinc-800/80">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 rounded-2xl shadow-inner">
                    <BookOpen className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-extrabold text-2xl text-zinc-900 dark:text-zinc-100 font-display">Sổ Tay Cá Nhân</h3>
                    <p className="text-sm text-zinc-500 font-medium mt-1">Bộ sưu tập mẫu câu và ý tưởng từ các bài học</p>
                  </div>
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto space-y-4 mb-8 pr-2 custom-scrollbar">
                {notebookItems.length > 0 ? (
                  notebookItems.map((item, idx) => (
                    <div key={idx} className="p-5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 dark:border-zinc-800/80 group hover:shadow-md transition-all duration-300">
                      <p className="text-base text-zinc-800 dark:text-zinc-200 whitespace-pre-wrap leading-relaxed">{item}</p>
                      <div className="mt-4 flex justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => {
                            const newItems = notebookItems.filter((_, i) => i !== idx);
                            setNotebookItems(newItems);
                            localStorage.setItem("vibe_collected_ideas", JSON.stringify(newItems));
                          }}
                          className="text-sm font-bold text-red-500 hover:text-red-700 flex items-center gap-2 bg-red-500/10 px-3 py-1.5 rounded-xl cursor-pointer transition-colors"
                        >
                          <Trash2 className="w-4 h-4" /> Xóa
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-20 opacity-60 font-bold border-2 border-dashed border-zinc-300 dark:border-zinc-700 rounded-3xl flex flex-col items-center justify-center">
                    <div className="p-6 bg-zinc-100 dark:bg-zinc-800 rounded-full mb-4">
                      <BookOpen className="w-10 h-10 text-zinc-400" />
                    </div>
                    <span className="text-lg text-zinc-600 dark:text-zinc-300">Sổ tay của bạn hiện đang trống.</span>
                    <span className="text-sm font-normal text-zinc-500 mt-2 max-w-sm">Bấm nút "Gom nhặt" khi đang học thẻ để lưu ý tưởng vào đây nhé!</span>
                  </div>
                )}
              </div>
              
              <div className="flex justify-end gap-3 pt-4">
                <button
                  onClick={() => {
                    if(confirm("Bạn có chắc chắn muốn xóa toàn bộ sổ tay? Dữ liệu không thể khôi phục.")) {
                      setNotebookItems([]);
                      localStorage.setItem("vibe_collected_ideas", "[]");
                    }
                  }}
                  disabled={notebookItems.length === 0}
                  className="px-6 py-3 bg-red-100 hover:bg-red-200 text-red-600 dark:bg-red-900/20 dark:hover:bg-red-900/40 rounded-xl font-bold text-sm transition disabled:opacity-50 cursor-pointer"
                >
                  Xóa tất cả
                </button>
                <button
                  onClick={() => {
                     const textToCopy = notebookItems.join("\\n\\n");
                     navigator.clipboard.writeText(textToCopy).then(() => {
                       toast.success(`Đã copy ${notebookItems.length} ý tưởng vào bộ nhớ đệm!`);
                     });
                  }}
                  disabled={notebookItems.length === 0}
                  className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold text-sm transition flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 cursor-pointer"
                >
                  <Copy className="w-4 h-4" /> Copy Toàn Bộ
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
"""

target = '      {activeTab === "settings" && ('
if "activeTab === \"notebook\"" not in content and target in content:
    content = content.replace(target, notebook_tab_content + "\n" + target)

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.write(content)
print("Inserted notebook tab content")
