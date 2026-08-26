import sys

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "r") as f:
    content = f.read()

# Replace simple error throws or console.error with dispatchTerminalLog in AI catch blocks
if "dispatchTerminalLog(`[AI AGENT] Lỗi khi gọi Agent: ${error.message || \"Không rõ\"}`, 'error');" not in content:
    # There are multiple catch (error: any) blocks, some might not be AI, but most are.
    # We will specifically target the catch blocks for the functions we patched above.
    
    # 1. hydrate-card
    hydrate_catch = """    } catch (error: any) {
      console.error(error);
      toast({
        title: "Lỗi kết nối",
        description: "Không thể tự động điền thông tin lúc này.",
        variant: "destructive",
      });
    } finally {"""
    hydrate_catch_new = """    } catch (error: any) {
      console.error(error);
      dispatchTerminalLog(`[AI AGENT ERROR] Lỗi Agent 1: ${error.message}`, 'error');
      toast({
        title: "Lỗi kết nối",
        description: "Không thể tự động điền thông tin lúc này.",
        variant: "destructive",
      });
    } finally {"""
    content = content.replace(hydrate_catch, hydrate_catch_new)
    
    # 2. translate-definition
    translate_catch = """    } catch (error: any) {
      console.error(error);
      toast({
        title: "Lỗi dịch thuật",
        description: "Không thể dịch định nghĩa lúc này.",
        variant: "destructive",
      });
    } finally {"""
    translate_catch_new = """    } catch (error: any) {
      console.error(error);
      dispatchTerminalLog(`[AI TRANSLATOR ERROR] Lỗi Dịch thuật: ${error.message}`, 'error');
      toast({
        title: "Lỗi dịch thuật",
        description: "Không thể dịch định nghĩa lúc này.",
        variant: "destructive",
      });
    } finally {"""
    content = content.replace(translate_catch, translate_catch_new)

with open("src/vibe-sandbox/VibeStudyRoom.tsx", "w") as f:
    f.write(content)
print("Patched VibeStudyRoom AI error logs")
