import React, { useState, useEffect, useRef } from 'react';
import { Terminal, X, Minimize2, Maximize2, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export type TerminalLog = {
  id: string;
  timestamp: Date;
  message: string;
  type: 'info' | 'warn' | 'error' | 'success';
};

export const dispatchTerminalLog = (message: string, type: 'info' | 'warn' | 'error' | 'success' = 'info') => {
  const event = new CustomEvent('vibe-terminal-log', {
    detail: { message, type }
  });
  window.dispatchEvent(event);
};

export const VibeTerminalOverlay: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [logs, setLogs] = useState<TerminalLog[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const endOfLogsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleLog = (e: Event) => {
      const customEvent = e as CustomEvent;
      const { message, type } = customEvent.detail;
      const newLog: TerminalLog = {
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date(),
        message,
        type
      };
      setLogs(prev => [...prev, newLog].slice(-100)); // Keep last 100 logs
      if (!isOpen || isMinimized) {
        setUnreadCount(prev => prev + 1);
      }
    };

    window.addEventListener('vibe-terminal-log', handleLog);
    return () => window.removeEventListener('vibe-terminal-log', handleLog);
  }, [isOpen, isMinimized]);

  useEffect(() => {
    if (isOpen && !isMinimized && endOfLogsRef.current) {
      endOfLogsRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, isOpen, isMinimized]);

  const toggleTerminal = () => {
    if (!isOpen) {
      setIsOpen(true);
      setIsMinimized(false);
      setUnreadCount(0);
    } else if (isMinimized) {
      setIsMinimized(false);
      setUnreadCount(0);
    } else {
      setIsOpen(false);
    }
  };

  const getLogColor = (type: string) => {
    switch (type) {
      case 'error': return 'text-red-400';
      case 'warn': return 'text-yellow-400';
      case 'success': return 'text-green-400';
      default: return 'text-zinc-300';
    }
  };

  const getPrefix = (type: string) => {
    switch (type) {
      case 'error': return '[ERROR]';
      case 'warn': return '[WARN]';
      case 'success': return '[SUCCESS]';
      default: return '[INFO]';
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        onClick={toggleTerminal}
        className="fixed bottom-6 left-6 z-[95] p-3 bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-green-400 rounded-full shadow-2xl transition-all duration-300 flex items-center justify-center group"
        title="Terminal System Logs"
      >
        <Terminal className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full border-2 border-zinc-900 animate-pulse">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {/* Terminal Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.95 }}
            animate={{ 
              opacity: 1, 
              y: 0, 
              scale: 1,
              height: isMinimized ? '48px' : '384px'
            }}
            exit={{ opacity: 0, y: 50, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className={`fixed bottom-24 left-6 z-[95] w-full max-w-lg bg-[#0a0a0a] border border-zinc-800 rounded-xl shadow-2xl overflow-hidden flex flex-col font-mono`}
          >
            {/* Terminal Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-zinc-900 border-b border-zinc-800 select-none cursor-pointer" onClick={() => setIsMinimized(!isMinimized)}>
              <div className="flex items-center gap-2 text-zinc-400 text-xs">
                <Terminal className="w-4 h-4 text-green-500" />
                <span className="font-semibold tracking-wider">UNITED_ENGINE_TERMINAL // v8.0</span>
              </div>
              <div className="flex items-center gap-3">
                <button 
                  onClick={(e) => { e.stopPropagation(); setLogs([]); }}
                  className="text-zinc-500 hover:text-red-400 transition-colors"
                  title="Clear Logs"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <button 
                  onClick={(e) => { e.stopPropagation(); setIsMinimized(!isMinimized); }}
                  className="text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  {isMinimized ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}
                </button>
                <button 
                  onClick={(e) => { e.stopPropagation(); setIsOpen(false); }}
                  className="text-zinc-500 hover:text-red-400 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Terminal Body */}
            {!isMinimized && (
              <div className="flex-1 p-4 overflow-y-auto custom-scrollbar text-xs leading-relaxed">
                {logs.length === 0 ? (
                  <div className="text-zinc-600 italic">Waiting for system events...</div>
                ) : (
                  logs.map((log) => (
                    <div key={log.id} className={`mb-1.5 break-words ${getLogColor(log.type)}`}>
                      <span className="text-zinc-500 mr-2">
                        [{log.timestamp.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}]
                      </span>
                      <span className="font-bold mr-2 opacity-80">{getPrefix(log.type)}</span>
                      <span>{log.message}</span>
                    </div>
                  ))
                )}
                <div ref={endOfLogsRef} />
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
