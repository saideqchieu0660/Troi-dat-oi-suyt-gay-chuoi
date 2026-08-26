import sys

with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "r") as f:
    content = f.read()

target = """    try {
      const res = await safeFetch("/api/vibe/generate-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: newGlobalTitle })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.prompt) {
          setNewGlobalPrompt(data.prompt);
          toast.success("Đã tạo prompt thành công!");
        } else {
          toast.error("Không thể tạo prompt, vui lòng thử lại.");
        }
      } else {
        toast.error("Lỗi kết nối khi tạo prompt.");
      }
    } catch (e) {
      console.error(e);
      toast.error("Đã xảy ra lỗi khi tạo prompt.");
    }"""

new_target = """    try {
      const { safeRequest } = await import("../utils/apiClient");
      const res = await safeRequest("/api/vibe/generate-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: newGlobalTitle })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.prompt) {
          setNewGlobalPrompt(data.prompt);
          toast.success("Đã tạo prompt thành công!");
        } else {
          toast.error("Không thể tạo prompt, vui lòng thử lại.");
        }
      } else {
        const errData = await res.json().catch(() => ({}));
        toast.error(errData.message || "Lỗi kết nối khi tạo prompt.");
      }
    } catch (e: any) {
      console.error(e);
      toast.error(e.message || "Đã xảy ra lỗi khi tạo prompt.");
    }"""

if "safeRequest" not in target: # just to be safe
    content = content.replace(target, new_target)
    with open("src/vibe-sandbox/VibeFlashcardActiveView.tsx", "w") as f:
        f.write(content)
    print("Patched VibeFlashcardActiveView.tsx")
