import sys

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    content = f.read()

import_statement = 'import { VibeTerminalOverlay } from "./VibeTerminalOverlay";'

if import_statement not in content:
    content = content.replace('import { VibeStudyEntryModal } from "./VibeStudyEntryModal";', 'import { VibeStudyEntryModal } from "./VibeStudyEntryModal";\n' + import_statement)
    
if "<VibeTerminalOverlay />" not in content:
    # Let's insert it before the closing </div> of the main dashboard container
    content = content.replace('      </AnimatePresence>\n    </div>\n  );\n}', '      </AnimatePresence>\n      <VibeTerminalOverlay />\n    </div>\n  );\n}')

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.write(content)
print("Patched dashboard with VibeTerminalOverlay")
