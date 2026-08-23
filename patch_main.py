import sys

with open('src/main.tsx', 'r') as f:
    content = f.read()

imports = """import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();"""

provider_start = """    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>"""
provider_end = """      </ErrorBoundary>
    </QueryClientProvider>"""

if 'QueryClientProvider' not in content:
    # insert imports
    content = content.replace("import { BrowserRouter } from 'react-router-dom';", "import { BrowserRouter } from 'react-router-dom';\n" + imports)
    
    # replace ErrorBoundary wrapper
    content = content.replace("<ErrorBoundary>", provider_start)
    content = content.replace("</ErrorBoundary>", provider_end)

    with open('src/main.tsx', 'w') as f:
        f.write(content)
    print("Patched main.tsx")
else:
    print("Already patched")
