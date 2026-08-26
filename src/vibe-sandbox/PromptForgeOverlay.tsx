import React, { useState, useEffect, useRef } from 'react';
import { X, Sparkles, Send, Loader2, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { diffWords } from 'diff';
import { safeRequest } from '../utils/apiClient';
import { toast } from 'sonner';

interface PromptForgeOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  initialTitle: string;
  initialRawPrompt: string;
  onApply: (finalPrompt: string) => void;
}

const DiffViewer = ({ oldText, newText }: { oldText: string, newText: string }) => {
  const differences = diffWords(oldText, newText);
  return (
    <div className="whitespace-pre-wrap font-mono text-sm leading-relaxed p-4 bg-zinc-50 dark:bg-zinc-950 rounded-lg border border-zinc-200 dark:border-zinc-800">
      {differences.map((part, index) => {
        const color = part.added 
          ? 'bg-green-200/60 dark:bg-green-900/40 text-green-900 dark:text-green-100 px-0.5 rounded' 
          : part.removed 
            ? 'bg-red-200/60 dark:bg-red-900/40 text-red-900 dark:text-red-100 line-through px-0.5 rounded opacity-70' 
            : 'text-zinc-800 dark:text-zinc-200';
        return <span key={index} className={color}>{part.value}</span>;
      })}
    </div>
  );
};

export const PromptForgeOverlay: React.FC<PromptForgeOverlayProps> = ({
  isOpen, onClose, initialTitle, initialRawPrompt, onApply
}) => {
  const [currentPrompt, setCurrentPrompt] = useState("");
  const [previousPrompt, setPreviousPrompt] = useState("");
  const [history, setHistory] = useState<{role: string, content: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const hasInitialized = useRef(false);

  useEffect(() => {
    if (isOpen && !hasInitialized.current) {
      hasInitialized.current = true;
      setPreviousPrompt(initialRawPrompt);
      generatePrompt();
    }
    if (!isOpen) {
      hasInitialized.current = false;
      setCurrentPrompt("");
      setHistory([]);
      setChatInput("");
    }
  }, [isOpen]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [currentPrompt, history, isGenerating]);

  const generatePrompt = async (newMessage?: string) => {
    setIsGenerating(true);
    try {
      const res = await safeRequest("/api/vibe/generate-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: initialTitle,
          rawPrompt: initialRawPrompt,
          history,
          newMessage
        })
      });
      
      const data = await res.json();
      if (data.success && data.prompt) {
        if (currentPrompt) {
          setPreviousPrompt(currentPrompt);
        }
        setCurrentPrompt(data.prompt);
        
        if (newMessage) {
          setHistory(prev => [
            ...prev, 
            { role: 'user', content: newMessage }, 
            { role: 'model', content: data.prompt }
          ]);
        } else {
          setHistory([{ role: 'model', content: data.prompt }]);
        }
        setChatInput("");
      } else {
        toast.error("Không thể tạo prompt. Vui lòng thử lại.");
      }
    } catch (error) {
      console.error(error);
      toast.error("Đã xảy ra lỗi khi kết nối với máy chủ.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmitChat = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || isGenerating) return;
    generatePrompt(chatInput);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        className="w-full max-w-4xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] h-[850px]"
      >
        {/* Header */}
        <div className="p-4 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between bg-zinc-50 dark:bg-zinc-900/50">
          <div className="flex items-center gap-2 text-purple-600 dark:text-purple-400">
            <Sparkles className="w-5 h-5" />
            <h3 className="font-semibold text-zinc-900 dark:text-zinc-100">Xưởng đúc Prompt (Prompt Forge)</h3>
          </div>
          <button onClick={onClose} className="text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 bg-zinc-50/30 dark:bg-zinc-950/30">
           
           <div className="bg-white dark:bg-zinc-900 p-4 rounded-lg border border-zinc-200 dark:border-zinc-800 text-sm text-zinc-600 dark:text-zinc-400 shadow-sm">
             <h4 className="font-medium text-zinc-900 dark:text-zinc-200 mb-2">Thông tin gốc:</h4>
             <p className="mb-1"><span className="font-semibold">Nhãn:</span> {initialTitle || "Chưa có tên"}</p>
             <p><span className="font-semibold">Nguyện vọng:</span> {initialRawPrompt || "Không có"}</p>
           </div>
           
           {/* History & Diffs */}
           <div className="space-y-6">
             {history.map((msg, idx) => {
                if (msg.role === 'user') {
                  return (
                    <div key={idx} className="flex justify-end">
                      <div className="bg-purple-100 dark:bg-purple-900/30 text-purple-900 dark:text-purple-100 px-4 py-2 rounded-2xl rounded-tr-sm max-w-[80%] text-sm">
                        {msg.content}
                      </div>
                    </div>
                  );
                }
                
                // For model responses, we only show diff for the LATEST model response compared to the PREVIOUS prompt.
                // Earlier history just shows the final text to save space.
                const isLatest = idx === history.length - 1;
                return (
                  <div key={idx} className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
                      <Sparkles className="w-3.5 h-3.5" />
                      AI Engineer {idx === 0 ? "Khởi tạo" : "Tinh chỉnh"}
                    </div>
                    {isLatest ? (
                      <DiffViewer oldText={previousPrompt} newText={msg.content} />
                    ) : (
                      <div className="p-4 bg-zinc-100 dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800 text-sm font-mono text-zinc-800 dark:text-zinc-200 opacity-60">
                        {msg.content}
                      </div>
                    )}
                  </div>
                );
             })}

             {isGenerating && (
               <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
                    <Sparkles className="w-3.5 h-3.5" />
                    Đang Đúc Prompt...
                  </div>
                  <div className="p-6 bg-zinc-50 dark:bg-zinc-950 rounded-lg border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-purple-600 dark:text-purple-400">
                    <Loader2 className="w-6 h-6 animate-spin" />
                  </div>
               </div>
             )}
           </div>

        </div>

        {/* Footer - Chat & Apply */}
        <div className="p-4 border-t border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
          <form onSubmit={handleSubmitChat} className="flex gap-2">
             <input 
               type="text" 
               value={chatInput}
               onChange={(e) => setChatInput(e.target.value)}
               placeholder="Gõ yêu cầu tinh chỉnh (VD: Làm cho nó ngắn hơn, đổi sang giọng hài hước...)" 
               disabled={isGenerating}
               className="flex-1 bg-zinc-100 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-700 rounded-lg px-4 py-2 text-sm text-zinc-900 dark:text-zinc-200 focus:outline-none focus:border-purple-500 dark:focus:border-purple-500 transition-colors disabled:opacity-50"
             />
             <button 
               type="submit" 
               disabled={!chatInput.trim() || isGenerating}
               className="bg-zinc-100 hover:bg-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 text-zinc-600 dark:text-zinc-300 p-2 rounded-lg transition-colors disabled:opacity-50"
             >
               <Send className="w-5 h-5" />
             </button>
             <div className="w-px bg-zinc-200 dark:bg-zinc-800 mx-1"></div>
             <button 
               type="button"
               disabled={!currentPrompt || isGenerating}
               onClick={() => onApply(currentPrompt)}
               className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-lg font-medium text-sm transition-colors whitespace-nowrap shadow-sm flex items-center gap-2 disabled:opacity-50"
             >
               Áp dụng Prompt <ArrowRight className="w-4 h-4" />
             </button>
          </form>
        </div>
      </motion.div>
    </div>
  );
}
