import sys

with open('src/utils/apiClient.ts', 'r') as f:
    content = f.read()

target = """if (typeof window !== "undefined") {
  setTimeout(syncProviderToggles, 1000);
  setInterval(syncProviderToggles, 30000); // Periodically check for remote API circuit breaker flips from administrator

  setTimeout(syncAIPrompts, 1500);
  setInterval(syncAIPrompts, 45000); // Periodically check for remote AI prompts adjustments
}"""

replacement = """// Config loading is now handled by React Query in App.tsx via useBatchConfig"""

content = content.replace(target, replacement)

# We still need a way to inject data into aiPromptsConfig
# aiPromptsConfig is already exported: export let aiPromptsConfig: any = {};
# and updateApiProviderConfig is exported: export function updateApiProviderConfig(newConfig: Partial<ApiProviderConfig>)

with open('src/utils/apiClient.ts', 'w') as f:
    f.write(content)
print("Patched apiClient.ts")
