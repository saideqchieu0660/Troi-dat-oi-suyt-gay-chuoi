import sys

with open("src/App.tsx", "r") as f:
    content = f.read()

import_statement = "import { useQueryClient } from '@tanstack/react-query';\n"
if "import { useQueryClient }" not in content:
    content = content.replace("import { useLeaderboard }", import_statement + "import { useLeaderboard }")

if "const queryClient = useQueryClient();" not in content:
    content = content.replace("const { data } = useBatchConfig();", "const queryClient = useQueryClient();\n  const { data } = useBatchConfig();")
    
if "vibe-sync-push-success" not in content:
    invalidate_effect = """
  useEffect(() => {
    const handleSyncSuccess = () => {
      queryClient.invalidateQueries({ queryKey: ['vibe-decks'] });
      queryClient.invalidateQueries({ queryKey: ['leaderboard'] });
    };
    window.addEventListener('vibe-sync-push-success', handleSyncSuccess);
    return () => window.removeEventListener('vibe-sync-push-success', handleSyncSuccess);
  }, [queryClient]);
"""
    content = content.replace("const { data } = useBatchConfig();", invalidate_effect + "\n  const { data } = useBatchConfig();")

with open("src/App.tsx", "w") as f:
    f.write(content)
