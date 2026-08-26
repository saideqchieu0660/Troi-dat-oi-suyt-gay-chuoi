import sys

with open("src/App.tsx", "r") as f:
    content = f.read()

target = """export default function App() {
  const location = useLocation();
  return (
    <ThemeProvider>
      <Toaster position="bottom-right" richColors />
      <GlobalErrorReporter />
      <AppConfigLoader />
      <Layout>"""

new_target = """import { VibeTerminalOverlay } from "./vibe-sandbox/VibeTerminalOverlay";

export default function App() {
  const location = useLocation();
  return (
    <ThemeProvider>
      <Toaster position="bottom-right" richColors />
      <GlobalErrorReporter />
      <AppConfigLoader />
      <VibeTerminalOverlay />
      <Layout>"""

if "VibeTerminalOverlay />" not in target: # check if already applied roughly
    content = content.replace(target, new_target)
    with open("src/App.tsx", "w") as f:
        f.write(content)
    print("Patched App.tsx")
