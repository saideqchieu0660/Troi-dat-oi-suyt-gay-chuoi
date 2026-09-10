import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', 'utf8');

const target1 = `const { hiddenSubjects } = useHiddenSubjects();`;
const replacement1 = `const { hiddenCategories: hiddenSubjects } = useHiddenSubjects();`;

if (content.includes(target1)) {
    content = content.replace(target1, replacement1);
    writeFileSync('src/vibe-sandbox/VibeStudentDashboard.tsx', content);
    console.log("Patched successfully");
} else {
    console.log("Not found target1");
}
