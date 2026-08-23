import sys

with open("src/main.tsx", "r") as f:
    content = f.read()

content = content.replace(
    "import { QueryClient, QueryClientProvider } from '@tanstack/react-query';",
    "import { QueryClient, QueryClientProvider } from '@tanstack/react-query';\nimport { ReactQueryDevtools } from '@tanstack/react-query-devtools';"
)

content = content.replace(
    "const queryClient = new QueryClient();",
    """const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 phút
      gcTime: 5 * 60 * 1000, // 5 phút
      refetchOnWindowFocus: false,
      retry: 2,
    },
  },
});"""
)

content = content.replace(
    "<App />\n        </SoundProvider>\n      </ErrorBoundary>\n    </QueryClientProvider>",
    "<App />\n        </SoundProvider>\n      </ErrorBoundary>\n      <ReactQueryDevtools initialIsOpen={false} />\n    </QueryClientProvider>"
)

with open("src/main.tsx", "w") as f:
    f.write(content)
