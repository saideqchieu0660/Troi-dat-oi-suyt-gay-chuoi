import sys, re

with open('server.ts', 'r') as f:
    content = f.read()

# Replace res.status(XXX).json({ error: ... }) inside catch blocks with next(err)
# But wait, not all route handlers have `next` in their signature!
# Express signature: async (req, res) => { ... } needs to become async (req, res, next) => { ... }
# Let's use a regex to ensure `next` is in the signature.
# This might be tricky with regex. Let's just do a string replacement for the common ones.

# First, add `next` to route signatures if they don't have it.
def add_next_to_signature(match):
    sig = match.group(0)
    if 'next' not in sig:
        if '(req, res)' in sig:
            return sig.replace('(req, res)', '(req, res, next)')
        elif '(req: express.Request, res: express.Response)' in sig:
            return sig.replace('(req: express.Request, res: express.Response)', '(req: express.Request, res: express.Response, next: express.NextFunction)')
    return sig

content = re.sub(r'app\.(get|post|put|delete)\("[^"]+",\s*(?:express\.json\(\),\s*)?async \([^)]+\) => \{', add_next_to_signature, content)

# Now replace the catch blocks
# catch (err: any) { res.status(...).json(...) } -> catch (err: any) { next(err); }

def replace_catch(match):
    catch_var = match.group(1)
    body = match.group(2)
    
    # Do not replace if it already has next(
    if 'next(' in body:
        return match.group(0)
    
    # Don't replace if it's the fallback cache block in translate-definition or global-prompts
    if 'appCache.getStale' in body:
        return match.group(0)
        
    # Replace res.status(...).json(...) with next(err)
    new_body = re.sub(r'res\.status\(\d+\)\.json\([^;]+\);?', f'next({catch_var});', body)
    # Also handle res.json({ error: ... }) without status
    new_body = re.sub(r'return res\.status\(\d+\)\.json\([^;]+\);?', f'return next({catch_var});', new_body)
    
    return f"catch ({catch_var}) {{{new_body}}}"

content = re.sub(r'catch \(([^)]+)\) \{([^}]+res\.(?:status|json)[^}]+)\}', replace_catch, content)

with open('server.ts', 'w') as f:
    f.write(content)
print("Routes patched")
