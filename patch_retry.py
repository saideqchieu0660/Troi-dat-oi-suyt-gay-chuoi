import sys

with open('server.ts', 'r') as f:
    content = f.read()

target = "async function executeGenerateContentRoundRobin(contents: any, config: any = {}): Promise<string> {"
replacement = """async function _executeGenerateContentRoundRobinInternal(contents: any, config: any = {}): Promise<string> {"""

if target in content:
    content = content.replace(target, replacement)
    
    wrapper = """
async function executeGenerateContentRoundRobin(contents: any, config: any = {}): Promise<string> {
  return withRetry(
    () => _executeGenerateContentRoundRobinInternal(contents, config),
    { maxRetries: 3, baseDelayMs: 2000, maxDelayMs: 15000 }
  );
}
"""
    # Insert the wrapper right above _executeGenerateContentRoundRobinInternal
    content = content.replace(replacement, wrapper + replacement)
    
    with open('server.ts', 'w') as f:
        f.write(content)
    print("Wrapped round robin with retry")
else:
    print("Not found")
