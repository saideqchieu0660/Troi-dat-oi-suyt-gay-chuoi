import re

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "r") as f:
    content = f.read()

# Add activeTier state
state_block = "const [isApplyingExplanation, setIsApplyingExplanation] = useState(false);"
new_state_block = state_block + "\n  const [activeTier, setActiveTier] = useState<number | null>(null);"
if state_block in content:
    content = content.replace(state_block, new_state_block)

# Replace handleFormatAI with handleProgressiveAssist
old_handle_format = r"""  const handleFormatAI = async \(e: React.MouseEvent\) => \{
    e\.stopPropagation\(\);
    if \(isFormatting \|\| !currentCard\) return;
    setIsFormatting\(true\);
    try \{
      const \{ safeRequest \} = await import\("\.\./utils/apiClient"\);
      const res = await safeRequest\("/api/automation/format-card", \{
        method: "POST",
        headers: \{ "Content-Type": "application/json" \},
        body: JSON\.stringify\(\{
          front: currentCard\.front \|\| "",
          back: currentCard\.back \|\| "",
          example_sentence: currentCard\.example_sentence \|\| "",
        \}\),
      \}\);

      if \(!res\.ok\) \{
        throw new Error\("Không thể kết nối AI định dạng\."\);
      \}

      const data = await res\.json\(\);
      setDiffFront\(data\.formattedFront \|\| currentCard\.front \|\| ""\);
      setDiffBack\(data\.formattedBack \|\| currentCard\.back \|\| ""\);
      setDiffExample\(data\.formattedExample \|\| currentCard\.example_sentence \|\| ""\);
      setIsFormatDiffModalOpen\(true\);
    \} catch \(err: any\) \{
      console\.warn\("Format AI Error:", err\);
      alert\("Không thể định dạng AI lúc này: " \+ \(err\.message \|\| "Lỗi kết nối\."\)\);
    \} finally \{
      setIsFormatting\(false\);
    \}
  \};"""

new_progressive = """  const handleProgressiveAssist = async (tier: number, prompt: string = "") => {
    if (activeTier !== null || !currentCard) return;
    setActiveTier(tier);
    try {
      const { safeRequest } = await import("../utils/apiClient");
      
      const res = await safeRequest("/api/vibe/card-progressive-assist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: currentCard.back || "",
          tier: tier,
          customPrompt: prompt
        }),
      });

      if (!res.ok) {
        throw new Error("Không thể kết nối Progressive API.");
      }

      const data = await res.json();
      
      let newBack = "";
      if (tier === 1) {
         newBack = `${currentCard.back || ""}\\n\\n<blockquote class="border-l-4 border-teal-500 bg-teal-50 dark:bg-teal-900/30 p-3 mt-4 rounded-r-lg"><b>🇻🇳 Dịch nghĩa:</b><br/>${data.translation}</blockquote>`;
      } else if (tier === 2) {
         newBack = `${data.formatted_content}\\n\\n<blockquote class="border-l-4 border-teal-500 bg-teal-50 dark:bg-teal-900/30 p-3 mt-4 rounded-r-lg"><b>🇻🇳 Dịch nghĩa:</b><br/>${data.translation}</blockquote>`;
      } else if (tier === 3) {
         newBack = `${data.formatted_content}\\n\\n<hr class="my-4 border-zinc-200 dark:border-zinc-700"/>\\n\\n<div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-800"><b>💡 AI Giải thích:</b><br/><div class="mt-2 text-sm">${data.explanation}</div></div>\\n\\n<hr class="my-4 border-zinc-200 dark:border-zinc-700"/>\\n\\n<blockquote class="border-l-4 border-teal-500 bg-teal-50 dark:bg-teal-900/30 p-3 rounded-r-lg"><b>🇻🇳 Dịch nghĩa:</b><br/>${data.translation}</blockquote>`;
      }

      setDiffFront(currentCard.front || "");
      setDiffBack(newBack.trim());
      setDiffExample(currentCard.example_sentence || "");
      setIsFormatDiffModalOpen(true);

    } catch (err: any) {
      console.warn("Progressive Assist Error:", err);
      alert("Lỗi AI: " + (err.message || "Lỗi kết nối."));
    } finally {
      setActiveTier(null);
      setShowAiDropdown(false);
      setIsCustomModalOpen(false);
    }
  };"""

content = re.sub(old_handle_format, new_progressive, content, flags=re.MULTILINE)

# Replace handleAutoClick
old_auto = r"""  const handleAutoClick = \(e: React\.MouseEvent\) => \{
    e\.stopPropagation\(\);
    onAgent3\(undefined, useProModel\);
    setShowAiDropdown\(false\);
  \};"""
new_auto = """  const handleAutoClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    handleProgressiveAssist(3);
  };"""
content = re.sub(old_auto, new_auto, content, flags=re.MULTILINE)

# Replace handleCustomSubmit
old_custom = r"""  const handleCustomSubmit = \(\) => \{
    if \(!customPrompt\.trim\(\)\) return;
    onAgent3\(customPrompt, useProModel\);
    setIsCustomModalOpen\(false\);
    setShowAiDropdown\(false\);
  \};"""
new_custom = """  const handleCustomSubmit = () => {
    if (!customPrompt.trim()) return;
    handleProgressiveAssist(3, customPrompt);
  };"""
content = re.sub(old_custom, new_custom, content, flags=re.MULTILINE)

# Replace the buttons:
# 1. Translate Button
old_translate_btn = r"""                onClick=\{\(e\) => \{ e\.stopPropagation\(\); onTranslateDefinition\(\); \}\}
                disabled=\{isTranslatingDefinition \|\| isExtracting \|\| isFormatting\}"""
new_translate_btn = """                onClick={(e) => { e.stopPropagation(); handleProgressiveAssist(1); }}
                disabled={activeTier !== null || isExtracting || isFormatting}"""
content = re.sub(old_translate_btn, new_translate_btn, content)

old_translate_text = r"""\{isTranslatingDefinition \? "Đang dịch\.\.\." : "Dịch định nghĩa"\}"""
new_translate_text = """{activeTier === 1 ? "Đang dịch..." : "Dịch định nghĩa"}"""
content = re.sub(old_translate_text, new_translate_text, content)

# 2. Format Button
old_format_btn = r"""onClick=\{handleFormatAI\}
              disabled=\{isFormatting \|\| isExtracting\}"""
new_format_btn = """onClick={(e) => { e.stopPropagation(); handleProgressiveAssist(2); }}
              disabled={activeTier !== null || isExtracting || isFormatting}"""
content = re.sub(old_format_btn, new_format_btn, content)

old_format_text = r"""\{isFormatting \? "Đang định dạng\.\.\." : "✨ Định dạng AI"\}"""
new_format_text = """{activeTier === 2 ? "Đang định dạng..." : "✨ Định dạng AI"}"""
content = re.sub(old_format_text, new_format_text, content)

# 3. Extract Button
old_extract_btn = r"""                onClick=\{\(e\) => \{ 
                  e\.stopPropagation\(\); 
                  if \(!isExtracting\) \{
                    setShowAiDropdown\(!showAiDropdown\);
                  \}
                \}\} 
                disabled=\{isExtracting\}"""
new_extract_btn = """                onClick={(e) => { 
                  e.stopPropagation(); 
                  if (activeTier === null && !isExtracting) {
                    setShowAiDropdown(!showAiDropdown);
                  }
                }} 
                disabled={activeTier !== null || isExtracting}"""
content = re.sub(old_extract_btn, new_extract_btn, content)

old_extract_text = r"""\{isExtracting \? "Đang suy nghĩ\.\.\." : "Giải thích AI"\}"""
new_extract_text = """{activeTier === 3 ? "Đang xử lý..." : "Giải thích AI"}"""
content = re.sub(old_extract_text, new_extract_text, content)

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "w") as f:
    f.write(content)

print("Patched VibeFlashcardActiveView.tsx successfully!")
