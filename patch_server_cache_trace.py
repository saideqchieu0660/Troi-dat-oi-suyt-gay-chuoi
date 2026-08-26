import sys

with open("server.ts", "r") as f:
    content = f.read()

# For translate-definition cache
translate_cache_target = """      const cachedData = appCache.get(cacheKey);
      if (cachedData) {
         return res.json({ translatedText: cachedData.translatedText });
      }"""

translate_cache_new = """      const cachedData = appCache.get(cacheKey);
      if (cachedData) {
         let traceLogs = [{ p: "system", s: "CACHE", m: "Truy xuất kết quả định nghĩa từ bộ nhớ đệm Cache (0đ/Không gọi API)" }];
         const store = asyncLocalStorage.getStore();
         if (store && store.res) {
             store.res.setHeader("X-AI-Trace", Buffer.from(JSON.stringify(traceLogs)).toString("base64"));
         }
         return res.json({ translatedText: cachedData.translatedText });
      }"""

if 'Truy xuất kết quả định nghĩa' not in content:
    content = content.replace(translate_cache_target, translate_cache_new)

# Are there other endpoints like Agent2 or Agent3 that use caching? Let's check `appCache` usage.
with open("server.ts", "w") as f:
    f.write(content)
print("Updated cache logic in server.")
