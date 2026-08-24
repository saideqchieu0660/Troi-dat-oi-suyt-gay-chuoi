import sys

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    content = f.read()

content = content.replace('| "united-engine"', '| "united-engine"\n    | "notebook"')

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.write(content)
print("Added notebook to activeTab type union")
