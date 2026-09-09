import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', 'utf8');

const hookLogic = `
  const [isPulling, setIsPulling] = useState(false);

  const pullCloudData = useCallback(async (showToast = false) => {
    if (!user) return;
    setIsPulling(true);
    if (showToast) {
       toast.loading("Đang kiểm tra tiến trình trên mây...", { id: "pull-sync" });
    }
    
    try {
      const count = await VibeSyncEngine.pullLatestCardStates(user.id);
      if (showToast) {
        if (count > 0) {
           toast.success(\`Đồng bộ thành công! Kéo về \${count} thay đổi từ thiết bị khác.\`, { id: "pull-sync" });
        } else {
           toast.success("Dữ liệu của bạn đã là mới nhất.", { id: "pull-sync" });
        }
      } else {
         if (count > 0) {
            toast.success(\`🎉 Đã tự động cập nhật \${count} thẻ từ thiết bị khác!\`);
         }
      }
    } catch (err) {
       if (showToast) toast.error("Không thể đồng bộ. Vui lòng kiểm tra kết nối.", { id: "pull-sync" });
    } finally {
       setIsPulling(false);
    }
  }, [user]);

  useEffect(() => {
    // Initial auto-pull
    pullCloudData(false);

    // Tab visibility auto-pull
    const handleVisibilityChange = () => {
       if (document.visibilityState === "visible") {
           pullCloudData(false);
       }
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, [pullCloudData]);

`;

if (!content.includes('pullCloudData = useCallback')) {
   content = content.replace('const prevLevelRef = useRef<number | null>(null);', 'const prevLevelRef = useRef<number | null>(null);\n' + hookLogic);
   writeFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', content);
   console.log("Patched successfully");
} else {
   console.log("Already patched");
}
