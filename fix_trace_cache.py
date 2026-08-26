import sys

with open("src/utils/apiClient.ts", "r") as f:
    content = f.read()

target = """            if (t.s === 'OK') {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI DISPATCHER] Xử lý THÀNH CÔNG bởi ${providerName} (Key: ${t.k})`, type: 'success' }
                }));
            }"""

new_target = """            if (t.s === 'OK') {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI DISPATCHER] Mạng lưới điều phối gọi THÀNH CÔNG mô hình từ ${providerName} (Key: ${t.k})`, type: 'success' }
                }));
            } else if (t.s === 'CACHE') {
                window.dispatchEvent(new CustomEvent('vibe-terminal-log', {
                  detail: { message: `[AI CACHE] ${t.m}`, type: 'success' }
                }));
            }"""

content = content.replace(target, new_target)

with open("src/utils/apiClient.ts", "w") as f:
    f.write(content)
print("Updated extractAITrace.")
