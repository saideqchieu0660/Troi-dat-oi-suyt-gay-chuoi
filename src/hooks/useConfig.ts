import { useQuery } from "@tanstack/react-query";

interface ApiToggles {
  groqEnabled: boolean;
  openRouterEnabled: boolean;
  geminiEnabled: boolean;
  deepInfraEnabled: boolean;
}

interface BatchConfigResponse {
  toggles: ApiToggles;
  prompts: Record<string, any>;
}

async function fetchBatchConfig(): Promise<BatchConfigResponse> {
  const res = await fetch("/api/config/batch");
  if (!res.ok) {
    throw new Error("Failed to fetch batch config");
  }
  return res.json();
}

export function useBatchConfig() {
  return useQuery({
    queryKey: ["app_config_batch"],
    queryFn: fetchBatchConfig,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
}

export function useAPIToggles() {
  const { data, isLoading, error } = useBatchConfig();
  return {
    toggles: data?.toggles || { groqEnabled: false, openRouterEnabled: false, geminiEnabled: true, deepInfraEnabled: false },
    isLoading,
    error,
  };
}

export function useAIPrompts() {
  const { data, isLoading, error } = useBatchConfig();
  return {
    prompts: data?.prompts || {},
    isLoading,
    error,
  };
}
