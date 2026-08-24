import sys

with open("src/services/next_gen/hybridRotationEngine.ts", "r") as f:
    content = f.read()

import_statement = 'import { dispatchTerminalLog } from "../../vibe-sandbox/VibeTerminalOverlay";\n'

if "dispatchTerminalLog" not in content:
    content = content.replace('import { store } from "../../lib/store";', 'import { store } from "../../lib/store";\n' + import_statement)

# Replace markKeyUsed
mark_used_orig = """  public markKeyUsed(keyString: string) {
    const key = this.systemKeys.find(k => k.key === keyString);
    if (key) {
      key.usageCount++;
      key.status = 'COOLING_DOWN';
      setTimeout(() => {
        if (key.status === 'COOLING_DOWN') {
          key.status = 'READY';
        }
      }, 12000);
    }
  }"""
mark_used_new = """  public markKeyUsed(keyString: string) {
    const key = this.systemKeys.find(k => k.key === keyString);
    if (key) {
      key.usageCount++;
      key.status = 'COOLING_DOWN';
      dispatchTerminalLog(`[KEY CYCLE] Assigned request to key: ${key.maskedKey}. Entering 12s cooldown.`, 'success');
      setTimeout(() => {
        if (key.status === 'COOLING_DOWN') {
          key.status = 'READY';
          dispatchTerminalLog(`[KEY CYCLE] Cooldown finished for key: ${key.maskedKey}. Ready for use.`, 'info');
        }
      }, 12000);
    }
  }"""
content = content.replace(mark_used_orig, mark_used_new)

# Replace isolateKey
isolate_orig = """  public isolateKey(keyString: string) {
    const key = this.systemKeys.find(k => k.key === keyString);
    if (key) {
      key.status = 'ISOLATED';
      setTimeout(() => {
        if (key.status === 'ISOLATED') {
          key.status = 'READY';
        }
      }, 60000);
    }
  }"""
isolate_new = """  public isolateKey(keyString: string) {
    const key = this.systemKeys.find(k => k.key === keyString);
    if (key) {
      key.status = 'ISOLATED';
      dispatchTerminalLog(`[CIRCUIT BREAKER] Key ${key.maskedKey} has been ISOLATED for 60 seconds due to errors/rate limits!`, 'error');
      setTimeout(() => {
        if (key.status === 'ISOLATED') {
          key.status = 'READY';
          dispatchTerminalLog(`[CIRCUIT BREAKER] Isolation ended for key: ${key.maskedKey}. Restored to pool.`, 'success');
        }
      }, 60000);
    }
  }"""
content = content.replace(isolate_orig, isolate_new)

with open("src/services/next_gen/hybridRotationEngine.ts", "w") as f:
    f.write(content)
print("Patched hybridRotationEngine")
