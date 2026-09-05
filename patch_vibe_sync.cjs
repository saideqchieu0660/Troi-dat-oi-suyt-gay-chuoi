const fs = require('fs');

let file = fs.readFileSync('src/vibe-sandbox/sync/VibeSyncRescue.ts', 'utf8');

file = file.replace(
  /console\.error\("Smart Pull Deck Error", error\);\s*throw error;/,
  `
    if (error?.message?.includes("offline") || error?.code === "unavailable" || String(error).includes("offline")) {
        console.warn("Smart Pull Deck Error: Client is offline. Pull skipped.");
        return "Skipped (Offline)";
    }
    console.error("Smart Pull Deck Error", error);
    throw error;
`
);

fs.writeFileSync('src/vibe-sandbox/sync/VibeSyncRescue.ts', file);
