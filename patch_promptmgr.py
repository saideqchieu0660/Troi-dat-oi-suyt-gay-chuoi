import sys

with open('src/services/next_gen/promptManager.ts', 'r') as f:
    content = f.read()

target = """  public async fetchFromDatabase() {
    this.isHydrating = true;
    try {
      const res = await fetch("/api/config/ai-prompts");
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) {
          const validData: any = {};
          for (const [key, val] of Object.entries(json.data)) {
            if (typeof val === 'string' && (val.length >= 20 || key === 'safetyDictionary')) {
              validData[key] = val;
            }
          }
          // Merge fetched data with defaults
          this.config = { ...this.config, ...validData };
          localStorage.setItem("nextgen_prompts_v2", JSON.stringify(this.config));
          this.updateSafetyRegex();
        }
      }
    } catch (e) {
      console.error("Failed to fetch dynamic prompts from server, falling back to cache", e);
    } finally {
      this.isHydrating = false;
    }
  }"""

replacement = """  public async fetchFromDatabase() {
    // Disabled direct fetch, config is injected via React Query from AppConfigLoader
  }
  
  public applyConfigFromNetwork(data: any) {
    if (!data) return;
    const validData: any = {};
    for (const [key, val] of Object.entries(data)) {
      if (typeof val === 'string' && (val.length >= 20 || key === 'safetyDictionary')) {
        validData[key] = val;
      }
    }
    this.config = { ...this.config, ...validData };
    localStorage.setItem("nextgen_prompts_v2", JSON.stringify(this.config));
    this.updateSafetyRegex();
  }"""

content = content.replace(target, replacement)

with open('src/services/next_gen/promptManager.ts', 'w') as f:
    f.write(content)
print("Patched promptManager")
