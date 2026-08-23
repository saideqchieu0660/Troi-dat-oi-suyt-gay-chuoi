import sys

with open('src/components/AIPromptsEditorWidget.tsx', 'r') as f:
    content = f.read()

# Replace imports
if "import { useAIPrompts } from '../hooks/useConfig';" not in content:
    content = content.replace('import { useEffect, useState } from "react";', 'import { useEffect, useState } from "react";\nimport { useAIPrompts } from "../hooks/useConfig";\nimport { useQueryClient } from "@tanstack/react-query";')

# Replace component logic
target_logic = """  const [prompts, setPrompts] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchPrompts = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/config/ai-prompts?t=${Date.now()}`);
      const data = await res.json();
      if (data && data.success) {
        setPrompts(data.data || {});
      }
    } catch (err: any) {
      setError(err.message || "Failed to load prompts");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, []);"""

replacement_logic = """  const { prompts: initialPrompts, isLoading: loading, error: fetchError } = useAIPrompts();
  const [prompts, setPrompts] = useState<any>({});
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    if (initialPrompts) {
      setPrompts(initialPrompts);
    }
    if (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : "Failed to load prompts");
    }
  }, [initialPrompts, fetchError]);"""

content = content.replace(target_logic, replacement_logic)

# Replace syncAIPrompts() call with queryClient.invalidateQueries
target_sync = """        setSuccess("Lưu System Prompts thành công! Server đã cập nhật đồng bộ.");
        syncAIPrompts();
        setTimeout(() => setSuccess(null), 3000);"""

replacement_sync = """        setSuccess("Lưu System Prompts thành công! Server đã cập nhật đồng bộ.");
        queryClient.invalidateQueries({ queryKey: ["app_config_batch"] });
        setTimeout(() => setSuccess(null), 3000);"""

content = content.replace(target_sync, replacement_sync)

with open('src/components/AIPromptsEditorWidget.tsx', 'w') as f:
    f.write(content)
print("Patched AIPromptsEditorWidget")
