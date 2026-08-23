import sys

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    content = f.read()

content = content.replace(
    "const rawDecks = useLiveVibeDecks();",
    "const { data: rawDecks = [] } = useLiveVibeDecks(user?.uid || user?.id);"
)

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.write(content)
