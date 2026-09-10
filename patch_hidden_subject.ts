import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/hooks/useHiddenSubjects.ts', 'utf8');
content = content.replace(/'system_config'/g, "'vibe_settings'");
content = content.replace(/'library_settings'/g, "'dashboard_config'");
content = content.replace(/hiddenSubjects/g, "hiddenCategories");
content = content.replace(/useHiddenCategories/g, "useHiddenSubjects"); // keep the function name the same for now to not break other files

writeFileSync('src/hooks/useHiddenSubjects.ts', content);
console.log("Patched successfully");
