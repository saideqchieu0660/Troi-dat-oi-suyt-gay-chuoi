import sys

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

import_statement = 'import { VibeTerminalOverlay } from "./VibeTerminalOverlay";'

if import_statement not in content:
    content = content.replace('import { VibeStudyCompanion } from "./VibeStudyCompanion";', 'import { VibeStudyCompanion } from "./VibeStudyCompanion";\n' + import_statement)
    
if "<VibeTerminalOverlay />" not in content:
    content = content.replace('    </>\n  );\n}', '      <VibeTerminalOverlay />\n    </>\n  );\n}')

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)
print("Patched VibeStudyRoom with VibeTerminalOverlay")
