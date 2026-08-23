import sys

with open('src/components/AIPromptsEditorWidget.tsx', 'r') as f:
    content = f.read()

# Fix imports
content = content.replace("import { syncAIPrompts } from '../utils/apiClient';", "")

with open('src/components/AIPromptsEditorWidget.tsx', 'w') as f:
    f.write(content)
