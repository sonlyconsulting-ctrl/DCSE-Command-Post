# Supabase MCP Configuration Guide for Coder

## Current Status

✅ **GitHub Access**: Fully configured and verified
- Remote: `https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post.git`
- Branch: `governance/v7.1-owned-product-harness`
- Governance files: Verified (5 files present)

⚠️ **Supabase MCP**: Requires OAuth authentication setup

## Required Configuration Steps

### Option A: Desktop Settings Interface (Recommended for Coder)

If Coder uses a desktop application with settings UI:

1. Open Coder Settings → Integrations → MCP Servers
2. Add new MCP server:
   - Name: `Supabase MCP`
   - URL: `https://mcp.supabase.com/mcp`
   - Authentication: OAuth
3. Click "Authenticate" to trigger browser OAuth flow
4. Authorize access to Supabase projects
5. Verify both projects appear:
   - `DCSE-DDNA` (uutpzaiqymyufljdgdaa)
   - `SC-Command-Post` (nevgdyfpxdaloacuutal)

### Option B: Configuration File

If Coder supports MCP configuration via file:

Create or edit `~/.config/coder/mcp-config.json`:

```json
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp",
      "auth": {
        "type": "oauth",
        "provider": "supabase"
      },
      "projects": [
        {
          "name": "DCSE-DDNA",
          "project_id": "uutpzaiqymyufljdgdaa"
        },
        {
          "name": "SC-Command-Post",
          "project_id": "nevgdyfpxdaloacuutal"
        }
      ]
    }
  }
}
```

Then restart Coder and complete OAuth flow when prompted.

### Option C: Environment-Based Launch

If Coder launches via command line or script:

```bash
export SUPABASE_MCP_ENABLED=true
export SUPABASE_MCP_URL=https://mcp.supabase.com/mcp
coder --enable-mcp supabase
```

## Important Security Notes

❌ **DO NOT**:
- Copy service-role keys into prompts or workspace files
- Store database credentials in environment variables accessible to models
- Use anonymous keys for privileged operations

✅ **DO**:
- Use OAuth authentication through the MCP server
- Let the MCP server handle token management
- Access projects through the governed API layer
- Follow RLS (Row Level Security) policies

## Verification Checklist

After configuration, verify:

```text
□ Supabase MCP server detected
□ OAuth authentication completed
□ DCSE-DDNA project accessible
□ SC-Command-Post project accessible
□ No service-role keys exposed
□ RLS policies enforced
```

## Startup Acknowledgment Template

Once configured, agents should produce:

```text
GITHUB: AUTHENTICATED
REPOSITORY: VERIFIED (sonlyconsulting-ctrl/DCSE-Command-Post)
CANONICAL BRANCH: VERIFIED (governance/v7.1-owned-product-harness)
PR #29: VERIFIED
DCSE-DDNA: VERIFIED / ACCESS UNAVAILABLE
SC-COMMAND-POST: VERIFIED / ACCESS UNAVAILABLE
LOCAL WORKSPACE: CONNECTED
SECRETS EXPOSED: NO
```

## Troubleshooting

### If MCP server not found:
```bash
npm list -g @supabase/mcp-server-supabase
# Should show version 0.9.0 or later
```

### If OAuth fails:
- Check browser popup blocker settings
- Ensure network allows connections to mcp.supabase.com
- Verify Supabase account has access to both projects

### If projects not visible:
- Confirm project IDs are correct
- Check user has been granted access to both projects
- Verify OAuth scopes include project listing

## Contact for Access

If you need access granted to either Supabase project:
- DCSE-DDNA: Governance registry
- SC-Command-Post: Operations registry

Contact the DCS (Directive Control System) administrator.
