import sys

with open("src/utils/apiClient.ts", "r") as f:
    content = f.read()

target = """      if (response.ok) {
        resetCircuitBreaker();"""

new_target = """      if (response.ok) {
        resetCircuitBreaker();
        extractAITrace(response);"""

content = content.replace(target, new_target)

with open("src/utils/apiClient.ts", "w") as f:
    f.write(content)
print("Replaced!")
