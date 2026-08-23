import sys

with open("src/components/ManualFlashcardImporter.tsx", "r") as f:
    content = f.read()

content = content.replace(
    "let completedCount = startChunk;",
    "const initialKeysStatus = await getKeysStatus();\n      let completedCount = startChunk;"
)

content = content.replace(
    "const currentKeys = await getKeysStatus();",
    "const currentKeys = initialKeysStatus; // Fixed: moved getKeysStatus outside loop"
)

with open("src/components/ManualFlashcardImporter.tsx", "w") as f:
    f.write(content)
