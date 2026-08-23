import { Request, Response, NextFunction } from 'express';

export function errorHandler(err: any, req: Request, res: Response, next: NextFunction) {
  console.error(`[Error] ${req.method} ${req.originalUrl}:`, err);

  const isDev = process.env.NODE_ENV !== "production";
  let statusCode = err.status || err.statusCode || 500;
  let message = err.message || "Internal Server Error";
  let errorCode = "UNKNOWN_ERROR";

  // 1. Firebase Errors (e.g. Quota Exceeded)
  if (err.code === 8 || err.code === 'resource-exhausted') {
    statusCode = 429;
    message = "Hệ thống đang quá tải tài nguyên (Quota Exceeded). Vui lòng thử lại sau.";
    errorCode = "RESOURCE_EXHAUSTED";
  } else if (err.code === 'permission-denied' || err.code === 7) {
    statusCode = 403;
    message = "Bạn không có quyền thực hiện hành động này.";
    errorCode = "PERMISSION_DENIED";
  }

  // 2. Groq/Gemini/OpenAI API Errors
  if (err.response) {
    const status = err.response.status;
    if (status === 429) {
      statusCode = 429;
      message = "Mô hình AI đang quá tải. Vui lòng đợi vài giây rồi thử lại.";
      errorCode = "AI_RATE_LIMIT";
    } else if (status === 404) {
      statusCode = 404;
      message = "Không tìm thấy mô hình hoặc dịch vụ AI.";
      errorCode = "AI_NOT_FOUND";
    } else if (status >= 500) {
      statusCode = status;
      message = "Dịch vụ AI đang gặp sự cố. Vui lòng thử lại sau.";
      errorCode = "AI_SERVER_ERROR";
    }
  } else if (err.message?.includes('fetch failed') || err.message?.includes('network')) {
    statusCode = 503;
    message = "Lỗi kết nối mạng đến dịch vụ AI. Vui lòng thử lại.";
    errorCode = "NETWORK_ERROR";
  }

  // Send Response
  const responsePayload: any = {
    error: true,
    errorCode,
    message,
    ...(isDev && { stack: err.stack }) // Only include stack in development
  };

  res.status(statusCode).json(responsePayload);
}
