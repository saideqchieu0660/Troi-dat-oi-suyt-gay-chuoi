import sys

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

retry_logic = """      let data;
      try {
        const res = await safeRequest("/api/agent3/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${idToken}`,
            "x-user-id": user?.id || "",
            "x-user-role": user?.role || "",
            "x-user-is-pro": user?.isPro ? "true" : "false",
          },
          body: JSON.stringify({
            message: promptToSend,
            context: contextualPrompt,
            mode: "flashcard_assist",
            responseMode: "direct",
            responseStyle: "concise",
            useProModel: useProModel
          }),
        });

        if (!res.ok) {
           throw new Error(await res.text());
        }
        const text = await res.text();
        data = JSON.parse(text);
      } catch (err: any) {
        // Fallback Retry
        toast.error(`Lỗi kết nối AI: ${err.message || err}. Đang xoay vòng API...`, { duration: 4000 });
        const res2 = await safeRequest("/api/agent3/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${idToken}`,
            "x-user-id": user?.id || "",
            "x-user-role": user?.role || "",
            "x-user-is-pro": user?.isPro ? "true" : "false",
          },
          body: JSON.stringify({
            message: promptToSend,
            context: contextualPrompt,
            mode: "flashcard_assist",
            responseMode: "direct",
            responseStyle: "concise",
            useProModel: useProModel,
            forcedProvider: "groq"
          }),
        });
        if (!res2.ok) {
           throw new Error(await res2.text());
        }
        const text = await res2.text();
        data = JSON.parse(text);
      }"""

old_logic = """      const res = await safeRequest("/api/agent3/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${idToken}`,
          "x-user-id": user?.id || "",
          "x-user-role": user?.role || "",
          "x-user-is-pro": user?.isPro ? "true" : "false",
        },
        body: JSON.stringify({
          message: promptToSend,
          context: contextualPrompt,
          mode: "flashcard_assist",
          responseMode: "direct",
          responseStyle: "concise",
          useProModel: useProModel
        }),
      });

      if (!res.ok) {
        let errData;
        try {
          const text = await res.text();
          errData = JSON.parse(text);
        } catch (e) {
          errData = { error: "Server Error: " + (e.message || "Invalid JSON") };
        }
        if (res.status === 429) {
          setDeepExplanation(
            `⏳ **Cooldown 20s**: ${errData.error || "Bạn đang gọi AI quá nhanh. Hãy chờ!"}`,
          );
          setIsExtracting(false);
          return;
        }
        throw new Error(errData.error || "Failed to query express backend");
      }

      let data;
        try {
          const text = await res.text();
          data = JSON.parse(text);
        } catch (e) {
          data = { result: "Server Error: " + (e.message || "Invalid JSON") };
        }"""

content = content.replace(old_logic, retry_logic)
with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)
