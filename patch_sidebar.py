import sys

with open("src/vibe-sandbox/VibeSidebar.tsx", "r") as f:
    content = f.read()

# Add to navItems
nav_item_notebook = """    {
      id: "notebook",
      label: "📓 Sổ Tay Cá Nhân",
      icon: BookOpen,
      action: () => handleSelectTab("notebook"),
    },
"""
# We'll insert it right after "Thư Viện"
target = """    {
      id: "library",
      label: "📚 Thư Viện",
      icon: Library,
      action: () => handleSelectTab("all_sets"),
    },"""

if "id: \"notebook\"" not in content:
    content = content.replace(target, target + "\n" + nav_item_notebook)

with open("src/vibe-sandbox/VibeSidebar.tsx", "w") as f:
    f.write(content)
print("Patched VibeSidebar")
