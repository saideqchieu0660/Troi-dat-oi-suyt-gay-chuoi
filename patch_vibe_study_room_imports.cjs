const fs = require('fs');
let file = fs.readFileSync('src/vibe-sandbox/VibeStudyRoom.tsx', 'utf8');

file = file.replace(/import\("\.\/sync\/VibeProgressSyncManager"\)\.then\(m => m\.VibeProgressSyncManager/g, "Promise.resolve(VibeProgressSyncManager).then(VibeProgressSyncManager => VibeProgressSyncManager");

fs.writeFileSync('src/vibe-sandbox/VibeStudyRoom.tsx', file);
