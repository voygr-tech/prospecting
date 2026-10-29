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
[Prospecting MCP server](https://api.voygr.tech/places/mcp). Sign in once in
your browser. You do not need to copy an API key for the plugin. The server
uses your VOYGR account and credit balance.

### Claude Code

Run inside Claude Code:

```
/plugin marketplace add voygr-tech/prospecting
/plugin install prospecting@prospecting
```

Choose user scope if prompted. Run `/mcp`, select `plugin:prospecting:places`, and sign in.
The skill answers to `/prospecting:prospecting`.

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

An MCP client that supports OAuth can connect directly to
`https://api.voygr.tech/places/mcp` using streamable HTTP.

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
