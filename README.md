# VOYGR Prospecting

Give your agent a lead list. Find US local businesses by city and category,
then enrich them: owners and key people with email and phone, legal entity,
open/closed status, hours, website, and any custom attribute you describe in
plain English ("does this jeweler sell lab-grown diamonds").

- 16M+ US places
- Searching and counting are free; you pay per place imported and **only for
  cells that get an answer**
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

The agent sizes the query for free, tells you the maximum cost, and asks
before spending.

## Use with PlaceCall

Build a list here, then have [PlaceCall](https://github.com/voygr-tech/placecall)
call the businesses on it (confirm details, ask a question, book). Same key,
same balance.

## API

Everything goes to `https://api.voygr.tech` with header `X-API-Key`. Full
reference: https://api.voygr.tech/docs. Public credit rates:
`GET https://api.voygr.tech/v1/pricing`.

## License

MIT
