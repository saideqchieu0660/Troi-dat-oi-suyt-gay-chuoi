import sys

with open("src/vibe-sandbox/VibeTerminalOverlay.tsx", "r") as f:
    content = f.read()

# The current buttons:
# <button onClick={(e) => { e.stopPropagation(); setLogs([]); }} className="text-zinc-500 hover:text-red-400 transition-colors" title="Clear Logs"><Trash2 className="w-3.5 h-3.5" /></button>
# <button onClick={(e) => { e.stopPropagation(); setIsMinimized(!isMinimized); }} className="text-zinc-500 hover:text-zinc-300 transition-colors">{isMinimized ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}</button>
# <button onClick={(e) => { e.stopPropagation(); setIsOpen(false); }} className="text-zinc-500 hover:text-red-400 transition-colors"><X className="w-4 h-4" /></button>

content = content.replace('w-3.5 h-3.5', 'w-5 h-5')
content = content.replace('w-4 h-4', 'w-5 h-5')
# Let's also add more padding to the buttons
content = content.replace('className="text-zinc-500 hover:text-red-400 transition-colors"', 'className="p-1.5 text-zinc-500 hover:text-red-400 transition-colors bg-zinc-800/50 hover:bg-zinc-800 rounded-md"')
content = content.replace('className="text-zinc-500 hover:text-zinc-300 transition-colors"', 'className="p-1.5 text-zinc-500 hover:text-zinc-300 transition-colors bg-zinc-800/50 hover:bg-zinc-800 rounded-md"')

with open("src/vibe-sandbox/VibeTerminalOverlay.tsx", "w") as f:
    f.write(content)
