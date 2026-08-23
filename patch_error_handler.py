import sys

with open('server.ts', 'r') as f:
    content = f.read()

# Add imports
imports = """import { errorHandler } from "./src/lib/errorHandler";
import { withRetry } from "./src/lib/withRetry";"""

if "import { errorHandler }" not in content:
    content = content.replace('import { appCache } from "./src/lib/firestore-cache";', 'import { appCache } from "./src/lib/firestore-cache";\n' + imports)

# Replace Global Error Handling Middleware
old_error_handler = """// Global Error Handling Middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error("Global Error Caught:", err);
  
  const statusCode = err.status || 500;
  const isDev = process.env.NODE_ENV === "development";
  
  if (isDev) {
    res.status(statusCode).json({
      error: true,
      message: err.message || "Internal Server Error",
      path: req.originalUrl,
      stack: err.stack
    });
  } else {
    // Production: Hide stack trace details, show generic error if it's a 500 without a safe message
    res.status(statusCode).json({
      error: true,
      message: err.statusCode === 429 ? "Too Many Requests" : (statusCode >= 500 ? "Internal Server Error" : err.message)
    });
  }
});"""

new_error_handler = """// Global Error Handling Middleware
app.use(errorHandler);"""

if "app.use(errorHandler);" not in content:
    content = content.replace(old_error_handler, new_error_handler)

with open('server.ts', 'w') as f:
    f.write(content)
print("Replaced global error handler.")
