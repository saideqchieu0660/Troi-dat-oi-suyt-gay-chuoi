import sys
import re

with open("src/components/DocumentConverter.tsx", "r") as f:
    content = f.read()

import_statement = 'import { dispatchTerminalLog } from "../vibe-sandbox/VibeTerminalOverlay";\n'

if "dispatchTerminalLog" not in content:
    content = content.replace('import { nextGenIngestionEngine } from "../services/next_gen/unifiedIngestionEngine";', 'import { nextGenIngestionEngine } from "../services/next_gen/unifiedIngestionEngine";\n' + import_statement)

# Now we need to insert dispatchTerminalLog before fetch to Gemini and after it succeeds, and on failure.
# 1. Fetch secured active key
# inside callGeminiStreamingAPI
key_fetch_target = """    const securedKey = keyData.key;

    // Set progression text with streaming details"""
key_fetch_new = """    const securedKey = keyData.key;
    const maskedKey = securedKey.substring(0, 4) + "***" + securedKey.substring(securedKey.length - 4);
    dispatchTerminalLog(`[GEMINI ROTATION] Server allocated active Gemini key: ${maskedKey}`, 'success');

    // Set progression text with streaming details"""
content = content.replace(key_fetch_target, key_fetch_new)

endpoint_fetch_target = """    const response = await fetch(endpoint, {"""
endpoint_fetch_new = """    dispatchTerminalLog(`[GEMINI ENGINE] Initiating direct stream generateContent request...`, 'info');
    const response = await fetch(endpoint, {"""
content = content.replace(endpoint_fetch_target, endpoint_fetch_new)

# Find catch blocks or error throws to log error
# There is throw new Error inside keyRes
key_res_error = """    if (!keyRes.ok) {
      throw new Error("""
key_res_error_new = """    if (!keyRes.ok) {
      dispatchTerminalLog(`[GEMINI ENGINE] Server denied key request (Status ${keyRes.status})`, 'error');
      throw new Error("""
content = content.replace(key_res_error, key_res_error_new)

key_data_error = """    if (!keyData.success || !keyData.key) {
      throw new Error("""
key_data_error_new = """    if (!keyData.success || !keyData.key) {
      dispatchTerminalLog(`[GEMINI ENGINE] Key pool exhausted or empty`, 'error');
      throw new Error("""
content = content.replace(key_data_error, key_data_error_new)

# In the while(true) loop or when finished parsing
# Let's find "return cards;" inside callGeminiStreamingAPI
return_cards = """    return cards;
  };"""
return_cards_new = """    dispatchTerminalLog(`[GEMINI ENGINE] Stream complete. Successfully extracted ${cards.length} flashcards.`, 'success');
    return cards;
  };"""
content = content.replace(return_cards, return_cards_new)

with open("src/components/DocumentConverter.tsx", "w") as f:
    f.write(content)
print("Patched DocumentConverter")
