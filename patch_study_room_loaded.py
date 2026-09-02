with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

# Add isPersonalStatesLoaded state
state_old = "const [personalCardStates, setPersonalCardStates] = useState<any[] | null>(null);"
state_new = "const [personalCardStates, setPersonalCardStates] = useState<any[] | null>(null);\n  const [isPersonalStatesLoaded, setIsPersonalStatesLoaded] = useState(false);"
content = content.replace(state_old, state_new)

# Update the load personal states useEffect
load_old = """          if (isMounted) {
            setPersonalCardStates(states);
          }
        } catch (e) {
          console.error("Failed to fetch study room card states:", e);
        }
      });
    });"""
load_new = """          if (isMounted) {
            setPersonalCardStates(states);
            setIsPersonalStatesLoaded(true);
          }
        } catch (e) {
          console.error("Failed to fetch study room card states:", e);
          if (isMounted) setIsPersonalStatesLoaded(true);
        }
      });
    });"""
content = content.replace(load_old, load_new)

if "!user) return;" in content:
    content = content.replace("!user) return;", "!user) { setIsPersonalStatesLoaded(true); return; }")

# Update the deck queue useEffect
queue_old = """  useEffect(() => {
    if (deck) {
      if (queueInitDeckIdRef.current === deck.id) return; // Prevent overwriting study state on background syncs"""
queue_new = """  useEffect(() => {
    if (deck && isPersonalStatesLoaded) {
      if (queueInitDeckIdRef.current === deck.id) return; // Prevent overwriting study state on background syncs"""
content = content.replace(queue_old, queue_new)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)

print("Patched VibeStudyRoom for loaded state!")
