interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

export class MemoryCache {
  private cache: Map<string, CacheEntry<any>> = new Map();
  private defaultTTL: number; // in milliseconds

  constructor(ttlMinutes: number = 5) {
    this.defaultTTL = ttlMinutes * 60 * 1000;
  }

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    const now = Date.now();
    if (now - entry.timestamp > this.defaultTTL) {
      return null; // Expired
    }
    
    return entry.data as T;
  }

  getStale<T>(key: string): T | null {
    // Returns data even if expired (useful for quota exceeded fallbacks)
    const entry = this.cache.get(key);
    return entry ? (entry.data as T) : null;
  }

  set<T>(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
}

export const appCache = new MemoryCache(5); // 5 minutes TTL
