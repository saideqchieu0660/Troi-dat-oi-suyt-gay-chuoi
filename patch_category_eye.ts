import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/pages/TeacherDashboard.tsx', 'utf8');

const target = `<h4 className="text-xs font-black uppercase tracking-widest text-orange-600 dark:text-orange-500 flex items-center gap-1.5">
                                    📂 {subject}{" "}
                                    <span className="opacity-60 text-[10px] font-bold font-mono">
                                      ({subjectDecks.length} bộ)
                                    </span>
                                  </h4>`;

const replacement = `<h4 className="text-xs font-black uppercase tracking-widest text-orange-600 dark:text-orange-500 flex items-center gap-1.5">
                                    📂 {subject}{" "}
                                    <span className="opacity-60 text-[10px] font-bold font-mono">
                                      ({subjectDecks.length} bộ)
                                    </span>
                                  </h4>
                                  <button
                                    type="button"
                                    title={hiddenCategories.includes(subject) ? "Đang ẩn với học viên. Nhấn để hiện." : "Đang hiện với học viên. Nhấn để ẩn."}
                                    onClick={(e) => toggleCategoryVisibility(subject, e)}
                                    className={\`ml-2 p-1.5 rounded-full transition-colors border-none cursor-pointer flex items-center justify-center \${hiddenCategories.includes(subject) ? 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-950 dark:text-red-400' : 'bg-emerald-100 text-emerald-600 hover:bg-emerald-200 dark:bg-emerald-950 dark:text-emerald-400'}\`}
                                  >
                                    {hiddenCategories.includes(subject) ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                  </button>`;

if (content.includes(target)) {
   content = content.replace(target, replacement);
   writeFileSync('src/pages/TeacherDashboard.tsx', content);
   console.log("Patched successfully");
} else {
   console.log("Not found target");
}
