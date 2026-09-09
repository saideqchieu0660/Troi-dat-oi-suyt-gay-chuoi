import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', 'utf8');

const target = `<div className="flex flex-wrap items-center gap-4">
                <div className="bg-zinc-900 dark:bg-zinc-100/20 text-orange-700 dark:text-orange-400 px-4 py-2 rounded-lg font-bold flex items-center gap-2 relative">
                  <TrendingUp className="w-5 h-5" />
                  Weekly Points: <AnimatedCounter value={user?.points || 0} />
                </div>
              </div>`;

const replacement = `<div className="flex flex-wrap items-center gap-4">
                <div className="bg-zinc-900 dark:bg-zinc-100/20 text-orange-700 dark:text-orange-400 px-4 py-2 rounded-lg font-bold flex items-center gap-2 relative">
                  <TrendingUp className="w-5 h-5" />
                  Weekly Points: <AnimatedCounter value={user?.points || 0} />
                </div>
                <button 
                  onClick={() => pullCloudData(true)} 
                  disabled={isPulling}
                  className={cn(
                    "bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 text-emerald-600 dark:text-emerald-400 px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 shadow-sm transition-all hover:scale-105 active:scale-95",
                    isPulling && "opacity-50 cursor-not-allowed grayscale"
                  )}
                  title="Kiểm tra đồng bộ tiến trình học mới nhất từ máy khác về thiết bị này"
                >
                  <RefreshCw className={cn("w-4 h-4", isPulling && "animate-spin")} />
                  {isPulling ? "Đang kéo mây..." : "Đồng bộ thủ công"}
                </button>
              </div>`;

if (content.includes('Weekly Points: <AnimatedCounter')) {
   content = content.replace(target, replacement);
   writeFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', content);
   console.log("Patched successfully");
} else {
   console.log("Not found target");
}
