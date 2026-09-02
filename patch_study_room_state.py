with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

state_old = "const [personalCardStates, setPersonalCardStates] = useState<any[]>([]);"
state_new = "const [personalCardStates, setPersonalCardStates] = useState<any[]>([]);\n  const [isPersonalStatesLoaded, setIsPersonalStatesLoaded] = useState(false);"
content = content.replace(state_old, state_new)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)

print("Added isPersonalStatesLoaded state")
