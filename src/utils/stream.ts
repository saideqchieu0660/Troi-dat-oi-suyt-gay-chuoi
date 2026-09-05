export async function processStream(
  response: Response,
  onChunk: (text: string) => void,
  onTrace?: (traceLogs: any[]) => void
): Promise<void> {
  if (!response.body) throw new Error("No response body for streaming");

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    let newlineIndex;
    
    while ((newlineIndex = buffer.indexOf('\n\n')) !== -1) {
      const line = buffer.slice(0, newlineIndex).trim();
      buffer = buffer.slice(newlineIndex + 2);

      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.type === "chunk" && data.text) {
             onChunk(data.text);
          } else if (data.type === "trace" && data.data && onTrace) {
             onTrace(data.data);
          } else if (data.type === "error") {
             throw new Error(data.error);
          } else if (data.type === "done") {
             return;
          }
        } catch (e) {
          console.error("Error parsing stream chunk", e, line);
        }
      }
    }
  }
}

export function parsePartialJson(jsonStr: string) {
  const result: Record<string, string> = {};
  
  const extractString = (key: string) => {
     const regex = new RegExp('"' + key + '"\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)');
     const match = jsonStr.match(regex);
     if (match) {
        try {
           return JSON.parse('"' + match[1] + '"');
        } catch(e) {
           return match[1].replace(/\\\\n/g, '\n').replace(/\\\\"/g, '"');
        }
     }
     return "";
  };
  
  result.translation = extractString("translation");
  result.formatted_content = extractString("formatted_content");
  result.explanation = extractString("explanation");
  
  return result;
}
