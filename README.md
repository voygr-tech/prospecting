# VOYGR Prospecting

Give your agent a lead list. Find US local businesses by city and category,
then enrich them: owners and key people with email and phone, legal entity,
open/closed status, hours, website, and any custom attribute you describe in
plain English ("does this jeweler sell lab-grown diamonds").

- 16M+ US places
- Count and five-place preview are free; paid search and search-backed list
  imports charge per place. Completed field lookups can be charged even when
  no answer is found; failed lookups are free.
- Results as a table in chat or a CSV export

## Install

The Claude Code and Codex plugins include this skill and connect the
[Prospecting MCP server](https://api.voygr.tech/places/mcp). Claude Chat,
Cowork, ChatGPT, and other MCP clients can connect to the same server. Sign in
once in your browser. You do not need to copy an API key for these connections.
The server uses your VOYGR account and credit balance.

### Claude Code

Run inside Claude Code:

```
/plugin marketplace add voygr-tech/prospecting
/plugin install prospecting@prospecting
```

Choose user scope if prompted. Run `/mcp`, select `plugin:prospecting:places`, and sign in.
The skill answers to `/prospecting:prospecting`.

### Cowork

Add the custom connector as described in [Claude Chat](#claude-chat). It is
available in Claude Chat, Cowork, and Claude Desktop after you sign in. You do
not need a terminal or an API key.

### Claude Chat

Add VOYGR Prospecting as a custom connector in claude.ai:

1. On a personal plan, open **Settings** > **Connectors** > **Add custom connector**.
   On a Team or Enterprise plan, an Owner adds it under **Organization settings**
   > **Connectors**; each member then signs in with their own VOYGR account.
2. Name it `VOYGR Prospecting` and enter
   `https://api.voygr.tech/places/mcp` as the URL. Keep the sign-in setting
   Claude detects.
3. Select **Add**, sign in with your VOYGR account, and allow access.

Select VOYGR Prospecting from the tools menu in a chat to use the `places_*`
tools. Ask Claude to count and preview matches, then check the charge with you
before each paid search or lookup.

### ChatGPT

Add VOYGR Prospecting as a custom MCP app in ChatGPT on the web. Custom apps
depend on your ChatGPT plan.

1. Open **Plugins**, then **+** > **Create plugin** > **Create MCP App**.
2. Name it `VOYGR Prospecting`, set the server URL to
   `https://api.voygr.tech/places/mcp`, and choose **OAuth** authentication.
   Leave the OAuth settings ChatGPT discovers as they are, accept the custom-app
   notice, and select **Create**.
3. Sign in with your VOYGR account. In a chat, select VOYGR Prospecting from
   the tools menu.

Ask ChatGPT to count and preview matches, then check the charge with you before
paid work.

### Codex

Run in your shell:

```sh
codex plugin marketplace add voygr-tech/prospecting
codex plugin add prospecting@prospecting
codex mcp login places
```

The last command opens browser sign-in. If Codex has no `plugin` command,
update Codex or use the API-key skill route below.

### Skill only, with an API key

`./install.sh` copies `skills/prospecting/SKILL.md` into Claude Code's skills
directory. It does not connect the MCP server. You can also copy that file
to `~/.claude/skills/prospecting/SKILL.md` or install it in Codex with
`$skill-installer`. For these routes, sign up at **https://app.voygr.tech**
and set `VOYGR_API_KEY` in the agent's environment:

```sh
export VOYGR_API_KEY=pk_live_...
```

One VOYGR account has one key and one credit balance for every VOYGR API.
If you already use [PlaceCall](https://github.com/voygr-tech/placecall), the
skill accepts `PLACECALL_API_KEY` as the same account key.

### Other MCP clients (Cursor, Windsurf, MCP Inspector, ...)

Point the client at `https://api.voygr.tech/places/mcp` using streamable HTTP
transport and sign in with OAuth. This connects the `places_*` tools. In clients
without the Prospecting skill, ask the agent to count and preview matches and
check the charge with you before paid work.

## Try it

> Find 20 independent jewelers in Austin, TX. For each, get the owner's name
> and email and whether they sell lab-grown diamonds.

The agent counts and previews the query for free, explains charges for paid
search, import, and enrichment, and asks before spending. For larger runs,
the MCP server also returns a credit quote and asks for confirmation.

## Use with PlaceCall

Build a list here, then have [PlaceCall](https://github.com/voygr-tech/placecall)
call the businesses on it (confirm details, ask a question, book). Both use
your VOYGR account and credit balance.

## API

Skill-only API requests go to `https://api.voygr.tech` with header `X-API-Key`;
CSV bytes go to the presigned upload URL without that header. The public
reference is at https://api.voygr.tech/docs; its prospecting coverage is still
being audited. Account-specific place and fill rates are at `GET /v1/usage`.
`GET /v1/pricing` does not cover search, list imports, or list fills.

## License

MIT
