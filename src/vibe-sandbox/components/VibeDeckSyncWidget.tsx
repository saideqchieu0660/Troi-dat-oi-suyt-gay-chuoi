import { useState, useEffect } from "react";
import { CloudUpload, CheckCircle, RefreshCcw, AlertTriangle } from "lucide-react";
import { smartPushDeck } from "../sync/VibeSyncRescue";

export function VibeDeckSyncWidget({ deckId }: { deckId: string }) {
  const [syncState, setSyncState] = useState<"idle" | "syncing" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const triggerSync = async () => {
    setSyncState("syncing");
    setErrorMsg("");
    try {
      await smartPushDeck(deckId);
      setSyncState("success");
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "Lỗi đồng bộ");
      setSyncState("error");
    }
  };

  useEffect(() => {
    // Auto-sync on mount
    triggerSync();
  }, [deckId]);

  return (
    <div className="bg-white/50 dark:bg-black/20 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-4 flex flex-col gap-3 animate-in fade-in zoom-in-95 mt-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {syncState === "syncing" && (
            <div className="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500 animate-pulse">
              <RefreshCcw className="w-4 h-4 animate-spin" />
            </div>
          )}
          {syncState === "success" && (
            <div className="w-8 h-8 rounded-full bg-green-500/10 flex items-center justify-center text-green-500">
              <CheckCircle className="w-4 h-4" />
            </div>
          )}
          {syncState === "error" && (
            <div className="w-8 h-8 rounded-full bg-red-500/10 flex items-center justify-center text-red-500">
              <AlertTriangle className="w-4 h-4" />
            </div>
          )}
          
          <div>
            <h4 className="font-bold text-sm">
              {syncState === "syncing" && "Đang đồng bộ tiến trình..."}
              {syncState === "success" && "Đã đồng bộ lên Mây"}
              {syncState === "error" && "Chưa thể đồng bộ"}
            </h4>
            <p className="text-xs opacity-60">
              {syncState === "syncing" && "Vui lòng đợi trong giây lát"}
              {syncState === "success" && "Tiến trình của bạn đã được lưu an toàn."}
              {syncState === "error" && "Đã lưu vào thiết bị. Có thể thử đẩy thủ công."}
            </p>
          </div>
        </div>

        <button
          onClick={triggerSync}
          disabled={syncState === "syncing"}
          className="px-4 py-2 bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 text-sm font-bold rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          <CloudUpload className="w-4 h-4" />
          Đẩy thủ công
        </button>
      </div>

      {syncState === "error" && errorMsg && (
        <div className="text-xs text-red-500 bg-red-500/10 p-2 rounded-lg">
          Chi tiết lỗi: {errorMsg}
        </div>
      )}
    </div>
  );
}
