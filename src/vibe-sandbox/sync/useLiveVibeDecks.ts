import { useQuery } from '@tanstack/react-query';

export function useLiveVibeDecks(userId: string | null | undefined, deckId?: string, role?: string) {
  return useQuery({
    queryKey: ['vibe-decks', userId, deckId, role],
    queryFn: async () => {
      if (!userId) return [];
      
      const roleParam = role ? `&role=${role}` : '';
      const deckParam = deckId ? `&deckId=${deckId}` : '';
      const res = await fetch(`/api/vibe/decks?userId=${userId}${deckParam}${roleParam}`);
      
      if (!res.ok) throw new Error('Failed to fetch decks');
      return res.json();
    },
    enabled: !!userId,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}
