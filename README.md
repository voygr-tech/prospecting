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

## Get a key

Sign up at **https://app.voygr.tech** (free trial), then:

```bash
export VOYGR_API_KEY=pk_live_...
```

One VOYGR account has one key and one credit balance for every VOYGR API.
If you already use [PlaceCall](https://github.com/voygr-tech/placecall), your
`PLACECALL_API_KEY` is the same key; the skill picks it up automatically.

## Install

**Claude Code (plugin, auto-updates):**

```
/plugin marketplace add voygr-tech/prospecting
/plugin install prospecting@prospecting
```

**Claude Code (manual):** `./install.sh`, or copy
`skills/prospecting/SKILL.md` to `~/.claude/skills/prospecting/SKILL.md`.

**Codex:** use the Codex plugin in `.codex-plugin/`, or point your agent at
`AGENTS.md`.

## Try it

> Find 20 independent jewelers in Austin, TX. For each, get the owner's name
> and email and whether they sell lab-grown diamonds.

The agent counts and previews the query for free, explains charges for paid
search, import, and enrichment, and asks before spending.

## Use with PlaceCall

Build a list here, then have [PlaceCall](https://github.com/voygr-tech/placecall)
call the businesses on it (confirm details, ask a question, book). Same key,
same balance.

## API

API requests go to `https://api.voygr.tech` with header `X-API-Key`; CSV bytes
go to the presigned upload URL without that header. The public
reference is at https://api.voygr.tech/docs; its prospecting coverage is still
being audited. Account-specific place and fill rates are at `GET /v1/usage`.
`GET /v1/pricing` does not cover search, list imports, or list fills.

## License

MIT
