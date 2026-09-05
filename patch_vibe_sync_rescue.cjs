const fs = require('fs');
let file = fs.readFileSync('src/vibe-sandbox/sync/VibeSyncRescue.ts', 'utf8');

if (!file.includes("import { VibeProgressSyncManager }")) {
   file = `import { VibeProgressSyncManager } from "./VibeProgressSyncManager";\n` + file;
}

file = file.replace(/const \{ VibeProgressSyncManager \} = await import\("\.\/VibeProgressSyncManager"\);/g, "");

fs.writeFileSync('src/vibe-sandbox/sync/VibeSyncRescue.ts', file);
