export interface RetryOptions {
  maxRetries?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
}

export async function withRetry<T>(
  operation: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const maxRetries = options.maxRetries ?? 3;
  const baseDelayMs = options.baseDelayMs ?? 500;
  const maxDelayMs = options.maxDelayMs ?? 10000;

  let attempt = 0;

  while (true) {
    try {
      return await operation();
    } catch (error: any) {
      attempt++;

      // Determine if error is retryable
      const isRetryable = isRetryableError(error);

      if (attempt > maxRetries || !isRetryable) {
        throw error;
      }

      // Calculate exponential backoff with jitter
      const delay = Math.min(
        maxDelayMs,
        baseDelayMs * Math.pow(2, attempt - 1) + Math.random() * 200
      );

      console.warn(`[Retry] Attempt ${attempt}/${maxRetries} failed: ${error.message}. Retrying in ${Math.round(delay)}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}

function isRetryableError(error: any): boolean {
  // 1. Network Errors (fetch failed, ECONNRESET, etc.)
  if (error.message?.includes('fetch failed') || error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') {
    return true;
  }

  // 2. Groq/Gemini HTTP Status Codes (429 Too Many Requests, 500/502/503/504 Server Errors)
  if (error.response) {
    const status = error.response.status;
    if (status === 429 || status >= 500) {
      return true;
    }
  }
  
  // 3. Rate limit messages in the error body directly
  if (error.message?.toLowerCase().includes("too many requests") || error.message?.toLowerCase().includes("rate limit")) {
    return true;
  }

  return false;
}
