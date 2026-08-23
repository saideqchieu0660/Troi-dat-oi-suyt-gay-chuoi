import { useQuery } from '@tanstack/react-query';

export const useLeaderboard = (enabled: boolean) => {
  return useQuery({
    queryKey: ['leaderboard'],
    queryFn: async () => {
      const res = await fetch('/api/users/leaderboard');
      if (!res.ok) throw new Error('Failed to fetch leaderboard');
      return res.json();
    },
    enabled: enabled,
    staleTime: 5 * 60 * 1000, // 5 phút
  });
};
