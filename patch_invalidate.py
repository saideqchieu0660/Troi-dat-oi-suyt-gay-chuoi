import sys

with open("src/vibe-sandbox/sync/VibeSyncEngine.ts", "r") as f:
    content = f.read()

import_statement = "import { QueryClient } from '@tanstack/react-query';\n"
if "import { QueryClient }" not in content:
    content = content.replace("import { collection", import_statement + "import { collection")

# We create a global query client instance here for invalidation, or use window.dispatchEvent
# It's cleaner to dispatch an event and let App or Main handle it, but for now we'll just use a small queryClient helper.
# Actually, the best way in a non-component file is to dispatch a custom event.
invalidate_code = """
      if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('vibe-sync-push-success'));
      }
"""

content = content.replace("await batch.commit();", "await batch.commit();" + invalidate_code)

with open("src/vibe-sandbox/sync/VibeSyncEngine.ts", "w") as f:
    f.write(content)
