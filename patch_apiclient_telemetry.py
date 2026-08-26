import sys

with open("src/utils/apiClient.ts", "r") as f:
    content = f.read()

# We need to find where safeRequest handles the response.
# Actually, safeRequest queues it up. processQueue() is the one executing fetch!
# Let's patch processQueue().
# Target:
#       if (response.status >= 400 && response.status < 500) {
# Before that, or when response is successful (e.g., if (response.ok) { resolve(response); return; })

# Looking at processQueue in apiClient.ts:
#       if (response.ok) {
#         handleSuccess();
#         resolve(response);
#         return;
#       }

target = """      if (response.ok) {
        handleSuccess();
        resolve(response);
        return;
      }"""

new_target = """      if (response.ok) {
        handleSuccess();
        
        // --- AI Telemetry Log Intercept ---
        try {
          const aiProvider = response.headers.get("X-AI-Provider");
          const aiKey = response.headers.get("X-AI-Key");
          if (aiProvider && typeof window !== "undefined") {
            const providerName = aiProvider.toUpperCase();
            window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
              detail: {
                message: `[AI DISPATCHER] Xử lý thành công bởi ${providerName} (Key sử dụng: ${aiKey || "Không xác định"})`,
                type: 'success'
              }
            }));
          }
        } catch(e) {}
        
        resolve(response);
        return;
      }"""

if "AI Telemetry Log Intercept" not in content:
    content = content.replace(target, new_target)
    with open("src/utils/apiClient.ts", "w") as f:
        f.write(content)
    print("Patched apiClient.ts for telemetry")
else:
    print("apiClient.ts already patched")
