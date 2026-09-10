import { readFileSync, writeFileSync } from 'fs';

let content = readFileSync('src/vibe-sandbox/VibeClasses.tsx', 'utf8');

const target1 = `const { hiddenSubjects, toggleHiddenSubject } = useHiddenSubjects();`;
const replacement1 = `const { hiddenCategories: hiddenSubjects, toggleHiddenSubject } = useHiddenSubjects();`;

if (content.includes(target1)) {
    content = content.replace(target1, replacement1);
    writeFileSync('src/vibe-sandbox/VibeClasses.tsx', content);
    console.log("Patched successfully");
} else {
    console.log("Not found target1");
}
