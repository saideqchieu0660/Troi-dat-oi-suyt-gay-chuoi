import sys

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

import_statement = "import { VibeDeckSyncWidget } from \"./components/VibeDeckSyncWidget\";\n"
if "VibeDeckSyncWidget" not in content:
    content = content.replace('import { DiffViewer } from "../components/DiffViewer";', import_statement + 'import { DiffViewer } from "../components/DiffViewer";')

old_block = """              </div>

              {/* Actions list */}
              <div className="flex flex-col gap-3">"""
new_block = """              </div>

              {deck?.id && <VibeDeckSyncWidget deckId={deck.id} />}

              {/* Actions list */}
              <div className="flex flex-col gap-3">"""
content = content.replace(old_block, new_block)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)
print("Patched!")
