import sys

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

import_statement = 'import { dispatchTerminalLog } from "./VibeTerminalOverlay";'
if "dispatchTerminalLog" not in content:
    # We already added the import in the previous patch, but let's check
    pass

# Patch hydrate-card
if "dispatchTerminalLog(`[AI AGENT] Gọi Agent 1: Auto-Fill (Hydrate) thông tin thẻ`, 'info');" not in content:
    content = content.replace(
        'const res = await safeRequest("/api/automation/hydrate-card", {',
        'dispatchTerminalLog(`[AI AGENT] Gọi Agent 1: Auto-Fill (Hydrate) thông tin thẻ`, \'info\');\n      const res = await safeRequest("/api/automation/hydrate-card", {'
    )

# Patch agent2 explain
if "dispatchTerminalLog(`[AI AGENT] Gọi Agent 2: Bắt đầu giải thích chuyên sâu`, 'info');" not in content:
    content = content.replace(
        'const res = await safeRequest("/api/agent2/explain", {',
        'dispatchTerminalLog(`[AI AGENT] Gọi Agent 2: Bắt đầu giải thích chuyên sâu`, \'info\');\n      const res = await safeRequest("/api/agent2/explain", {'
    )

# Patch agent3 chat
if "dispatchTerminalLog(`[AI AGENT] Gọi Agent 3: Bắt đầu Chatbot AI`, 'info');" not in content:
    content = content.replace(
        'const res = await safeRequest("/api/agent3/chat", {',
        'dispatchTerminalLog(`[AI AGENT] Gọi Agent 3: Bắt đầu Chatbot AI`, \'info\');\n      const res = await safeRequest("/api/agent3/chat", {'
    )
    
if "dispatchTerminalLog(`[AI AGENT] Gửi đánh giá cho Agent 3`, 'info');" not in content:
    content = content.replace(
        'const res2 = await safeRequest("/api/agent3/chat", {',
        'dispatchTerminalLog(`[AI AGENT] Gửi đánh giá cho Agent 3`, \'info\');\n        const res2 = await safeRequest("/api/agent3/chat", {'
    )

# Patch translate-definition
if "dispatchTerminalLog(`[AI TRANSLATOR] Gọi API Dịch thuật định nghĩa`, 'info');" not in content:
    content = content.replace(
        'const res = await safeRequest("/api/vibe/translate-definition", {',
        'dispatchTerminalLog(`[AI TRANSLATOR] Gọi API Dịch thuật định nghĩa`, \'info\');\n      const res = await safeRequest("/api/vibe/translate-definition", {'
    )

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)
print("Patched VibeStudyRoom AI logs")
