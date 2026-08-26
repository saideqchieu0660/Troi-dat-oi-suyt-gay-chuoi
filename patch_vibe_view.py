import sys
import re

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "r") as f:
    content = f.read()

# 1. Add import for PromptForgeOverlay
if "PromptForgeOverlay" not in content:
    import_match = re.search(r"import\s+.*?\s+from\s+['\"].*?['\"];?", content)
    if import_match:
        content = content[:import_match.end()] + "\nimport { PromptForgeOverlay } from './PromptForgeOverlay';" + content[import_match.end():]

# 2. Add state inside VibeFlashcardActiveView
if "const [isForgeOpen, setIsForgeOpen]" not in content:
    state_match = re.search(r"const \[isGeneratingPrompt, setIsGeneratingPrompt\] = useState\(false\);", content)
    if state_match:
         content = content[:state_match.end()] + "\n  const [isForgeOpen, setIsForgeOpen] = useState(false);" + content[state_match.end():]

# 3. Change the button onClick
button_pattern = r'onClick=\{handleGeneratePrompt\}[\s\S]*?disabled=\{!newGlobalTitle.trim\(\) \|\| isGeneratingPrompt\}'
new_button = 'onClick={() => {\n                        if (!newGlobalTitle.trim()) { toast.error("Vui lòng nhập Tên nhãn trước"); return; }\n                        setIsForgeOpen(true);\n                      }}\n                      disabled={!newGlobalTitle.trim()}'

content = re.sub(button_pattern, new_button, content)

# 4. Inject the PromptForgeOverlay at the end before final </div> or </AnimatePresence>
# Wait, this is inside VibeFlashcardActiveView which returns AnimatePresence. I'll just put it before the last </div>
if "PromptForgeOverlay isOpen" not in content:
    last_div = content.rfind("</div>")
    if last_div != -1:
         overlay = """
      <PromptForgeOverlay 
        isOpen={isForgeOpen} 
        onClose={() => setIsForgeOpen(false)} 
        initialTitle={newGlobalTitle} 
        initialRawPrompt={newGlobalPrompt} 
        onApply={(finalPrompt) => {
           setNewGlobalPrompt(finalPrompt);
           setIsForgeOpen(false);
        }}
      />
"""
         content = content[:last_div] + overlay + content[last_div:]

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "w") as f:
    f.write(content)

print("Patched VibeFlashcardActiveView.tsx")
