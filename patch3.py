import sys

with open('server.ts', 'r') as f:
    content = f.read()

import_statement = 'import { appCache } from "./src/lib/firestore-cache";\n'
if import_statement not in content:
    content = content.replace('import { executeGroqRequest } from "./src/lib/groq";', 'import { executeGroqRequest } from "./src/lib/groq";\n' + import_statement)
    with open('server.ts', 'w') as f:
        f.write(content)
        print("Import added")
else:
    print("Import already exists")
