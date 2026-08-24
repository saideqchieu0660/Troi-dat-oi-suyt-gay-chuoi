import sys

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "r") as f:
    lines = f.readlines()

# Find the block and remove it
new_lines = []
skip = False
hook_lines = []
for i, line in enumerate(lines):
    if line.strip() == "useEffect(() => {" and "if (activeTab === \"notebook\") {" in "".join(lines[i:i+3]):
        skip = True
    
    if skip:
        hook_lines.append(line)
        if line.strip() == "}, [activeTab]);":
            skip = False
    else:
        new_lines.append(line)

# Re-insert the hook lines after activeTab state declaration finishes
final_lines = []
in_activeTab = False
for line in new_lines:
    final_lines.append(line)
    if "const [activeTab, setActiveTab] = useState<" in line:
        in_activeTab = True
    if in_activeTab and ");" in line.strip():
        in_activeTab = False
        # Insert hook
        final_lines.append("\n")
        final_lines.extend(hook_lines)

with open("src/vibe-sandbox/VibeStudentDashboard.tsx", "w") as f:
    f.writelines(final_lines)
print("Fixed initialization order!")
