---
name: prospecting
description: Find US local businesses and enrich them into a lead list - owners and key people with contacts, legal entity, open/closed status, hours, website, and any custom attribute you describe in plain English ("does this jeweler sell lab-grown diamonds"). 16M+ US places. You pay only for cells that get an answer.
license: MIT
compatibility: Needs curl and outbound HTTPS to api.voygr.tech, the only host this skill contacts and the only place it sends VOYGR_API_KEY. US places only.
metadata:
  version: "0.1.0"
  author: voygr-tech
  openclaw:
    primaryEnv: VOYGR_API_KEY
    requires:
      env:
        - VOYGR_API_KEY
    homepage: https://github.com/voygr-tech/prospecting
    tags: [prospecting, leads, enrichment, local-business, places, owners, b2b]
---

# VOYGR Prospecting

Turn "find me X in Y and tell me Z about each" into a structured lead list.
Search a US geography and category, save the matches as a list, then fill
the fields the user wants. Every request goes to `https://api.voygr.tech`
with header `X-API-Key: $VOYGR_API_KEY`.

## Setup

One VOYGR account has one key and one credit balance for every VOYGR API
(prospecting and PlaceCall calling). Resolve the key in this order:

1. `VOYGR_API_KEY` if set.
2. Otherwise `PLACECALL_API_KEY` if set (same account key, set by the
   PlaceCall skill). Each command runs in its own shell, so do the fallback
   in the SAME command as the request:
   `export VOYGR_API_KEY="$PLACECALL_API_KEY" && curl ...`.
3. Otherwise tell the user to sign up at https://app.voygr.tech (free trial)
   and `export VOYGR_API_KEY=pk_live_...`.

Never print the key. If a call returns `403`, the key exists but lacks
access to prospecting; the user should sign in once at https://app.voygr.tech
with the same email, which adds prospecting to the same key.

## Money rules (follow these every time)

- Searching, counting, field suggestions and pricing are **free**. Importing
  places into a list costs credits **per place imported**; filling costs
  credits **per answered cell**. Cells with no answer are free.
- Before any paid step, **state the maximum cost and get the user's OK**:
  places x rate for imports, rows x fields for fills. Read rates from
  `GET /v1/pricing` (no key needed) and the balance from `GET /v1/usage`.
- Start small: default to **20 places** unless the user asks for more. Never
  import "all matches" without an explicit number from the user.

## Workflow

### 1. Resolve the geography (free)

```bash
curl -s "https://api.voygr.tech/v1/geo/suggest?q=Austin%20TX&limit=5" -H "X-API-Key: $VOYGR_API_KEY"
```

Use the returned `geography_id` (e.g. `city:TX:austin`). Ask the user if the
match is ambiguous.

### 2. Pick categories (free)

```bash
curl -s https://api.voygr.tech/v1/places/categories -H "X-API-Key: $VOYGR_API_KEY"
```

Categories are taxonomy tags like `amenity=restaurant`. If the category list
looks thin for a vertical, also try a name filter `q` (e.g. `"q": "jewel"`)
and compare counts in step 3.

### 3. Size the query before spending (free)

```bash
curl -s -X POST https://api.voygr.tech/v1/places/count -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"geography_id":"city:TX:austin","categories":["shop=jewelry"],"independents_only":true}'
```

`independents_only: true` drops national chains, which have no reachable
local owner. Report the count to the user and agree on a limit.

### 4. Turn the user's question into fields (free)

```bash
curl -s -X POST https://api.voygr.tech/v1/fields/suggest -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"goal":"owner name and email, and whether they sell lab-grown diamonds"}'
```

The response is already in the shape a fill job accepts. Anything listed as
unsupported cannot be delivered; tell the user instead of trying.

### 5. Save the places as a list (paid: per place imported)

```bash
curl -s -X POST https://api.voygr.tech/v1/lists -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Austin jewelers","search":{"geography_id":"city:TX:austin","categories":["shop=jewelry"],"independents_only":true,"limit":20}}'
```

Keep the returned `list_id`. A user's own CSV can be used instead of a
search (`POST /v1/lists/upload-url`, then `POST /v1/lists` with `upload_key`).

### 6. Fill the fields (paid: per answered cell)

```bash
curl -s -X POST https://api.voygr.tech/v1/jobs/deep-research -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" -H "Idempotency-Key: <job-key>" \
  -d '{"list_id":"<list_id>","row_count":20,"fields":[
        {"name":"owners","include":["email","phone"]},
        {"name":"lab_grown_diamonds","description":"whether this jeweler sells lab-grown diamonds","value_type":"bool"}]}'
```

- `row_count` must equal the number of rows targeted (the list size, or the
  length of `row_ids`).
- `owners` returns the individual owner(s) as one value, `{name, role}` plus
  any contacts in `include` (each contact is one more credit per row).
  `owner_org` covers businesses owned by a company; `key_people` covers
  leadership beyond the owner.
- Custom fields: give a short `name`, a one-sentence `description`, and a
  `value_type` (`bool`, `enum` with `allowed_values`, `string`, `number`).
- The reserve is `row_count x fields`; you are charged only for filled cells.
- Re-run only what is missing with `"skip_filled": true`, or retry specific
  rows with `row_ids`.
- `Idempotency-Key`: generate ONE value per job (e.g. `uuidgen`) before the
  first submit and reuse that exact value on any retry of the same job. A new
  value on retry creates and charges a second job.

### 7. Read results

Poll the list; cells fill in as rows complete (poll every ~10 s, not faster):

```bash
curl -s "https://api.voygr.tech/v1/lists/<list_id>?limit=100" -H "X-API-Key: $VOYGR_API_KEY"
```

Export the whole list as CSV when done:

```bash
curl -s "https://api.voygr.tech/v1/lists/<list_id>/export" -H "X-API-Key: $VOYGR_API_KEY" -o leads.csv
```

Multi-valued columns are joined with `; ` and keep empty slots aligned.

## Presenting results

Summarize as a table: place, address, the requested fields. Say how many
cells came back empty ("no answer" is a normal, free outcome) and what the
run cost. Offer the CSV path.

## Errors

- `402`: out of credits. Tell the user to top up in the app.
- `403`: the key lacks access to prospecting; the user should sign in once at
  https://app.voygr.tech with the same email (adds prospecting to the key).
- `400` with a message: show the message; usually a bad geography, category
  or `row_count` mismatch.
- Places outside the US are not covered.
