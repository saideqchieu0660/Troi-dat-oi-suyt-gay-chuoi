import sys

with open("src/vibe-sandbox/sync/useLiveVibeDecks.ts", "w") as f:
    f.write("""import { useQuery } from '@tanstack/react-query';

export function useLiveVibeDecks(userId: string | null | undefined, deckId?: string) {
  return useQuery({
    queryKey: ['vibe-decks', userId, deckId],
    queryFn: async () => {
      if (!userId) return [];
      
      const res = await fetch(`/api/vibe/decks?userId=${userId}${deckId ? `&deckId=${deckId}` : ''}`);
      if (!res.ok) throw new Error('Failed to fetch decks');
      return res.json();
    },
    enabled: !!userId,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}
""")
