const fs = require('fs');
const file = 'src/pages/LegacyStudyRoom.tsx';
let content = fs.readFileSync(file, 'utf8');

const targetStr = `      let data;
        try {
          const text = await res.text();
          data = JSON.parse(text);
        } catch (e) {
          data = { result: "Server Error: " + (e.message || "Invalid JSON") };
        }
      setDeepExplanation(data.result);
    } catch (e: any) {
      setDeepExplanation(
        "Failed to agent 3 extract. Check AI connection. Error: " +
          (e.message || e),
      );
    }`;

const replaceStr = `
        let accumulated = "";
        setDeepExplanation(accumulated);
        await import("../utils/stream").then(async ({ processStream }) => {
            await processStream(res, (chunk) => {
               accumulated += chunk;
               setDeepExplanation(accumulated);
            });
        });
    } catch (e: any) {
      setDeepExplanation(
        "Lỗi kết nối AI: " +
          (e.message || e),
      );
    }`;

content = content.replace(targetStr, replaceStr);

fs.writeFileSync(file, content);
