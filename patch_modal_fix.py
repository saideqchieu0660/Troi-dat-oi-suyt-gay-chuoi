import sys

with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "r") as f:
    content = f.read()

bad_block = """                </p>
                </p>
              </div>"""
good_block = """                </div>
              </div>"""

content = content.replace(bad_block, good_block)
content = content.replace('<p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 flex items-center gap-2">', '<div className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 flex items-center gap-2">')

with open("src/vibe-sandbox/VibeStudyEntryModal.tsx", "w") as f:
    f.write(content)
print("Patched fixing JSX errors")
