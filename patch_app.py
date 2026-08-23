import sys

with open('src/App.tsx', 'r') as f:
    content = f.read()

imports = """import { useBatchConfig } from "./hooks/useConfig";
import { updateApiProviderConfig, aiPromptsConfig } from "./utils/apiClient";
import { nextGenPromptManager } from "./services/next_gen/promptManager";
import { useEffect } from "react";

function AppConfigLoader() {
  const { data } = useBatchConfig();
  
  useEffect(() => {
    if (data) {
      updateApiProviderConfig({
        openRouter: data.toggles.openRouterEnabled !== false,
        gemini: data.toggles.geminiEnabled !== false,
        groq: data.toggles.groqEnabled !== false,
        deepInfra: data.toggles.deepInfraEnabled !== false,
      });
      Object.assign(aiPromptsConfig, data.prompts);
      nextGenPromptManager.applyConfigFromNetwork(data.prompts);
    }
  }, [data]);
  
  return null;
}
"""

if "function AppConfigLoader" not in content:
    content = content.replace("export default function App() {", imports + "\nexport default function App() {")
    content = content.replace("<GlobalErrorReporter />", "<GlobalErrorReporter />\n      <AppConfigLoader />")
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Patched App.tsx")
else:
    print("Already patched")
