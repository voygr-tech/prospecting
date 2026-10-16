---
name: prospecting
description: Use when finding US local businesses by geography or category, importing a place CSV, or enriching a saved list with owners, contacts, business details, or custom research fields.
license: MIT
compatibility: Needs curl and outbound HTTPS to api.voygr.tech; CSV import also posts the file to the returned presigned upload URL. Send VOYGR_API_KEY only to api.voygr.tech. US places only.
metadata:
  version: "0.1.2"
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
the fields the user wants. API requests go to `https://api.voygr.tech`
with header `X-API-Key: $VOYGR_API_KEY`. CSV bytes go to a presigned upload
URL; never send the API key to that URL.

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

- Geography suggestions, categories, count, the five-place preview, field
  suggestions and CSV upload are free. `POST /v1/places/search` costs credits
  per returned place. A search-backed list costs credits per place imported,
  even if those places were already returned by a paid search. A CSV upload
  of the user's own places is free.
- A list fill reserves credits at submit. Completed lookups are charged at
  each field's price whether they find a value or abstain; failed lookups are
  free. Unused reservation is released when the job settles; check the job
  after cancellation too. Do not describe an empty cell as free without
  checking its job status.
- Before a paid request, explain its possible charge and get the user's OK.
  Use `GET /v1/usage` for the account's balance, `credits_per_place` and
  `credits_per_field`. `GET /v1/pricing` does **not** quote list or search
  rates. List fields have different prices, so do not estimate a fill by
  multiplying rows by the number of fields. In this skill's pricing version,
  `owners` is 2 field-price units per row for name and role; direct email adds
  1, phone adds 2, and a custom field defaults to 3. Other presets can cost
  more. The public rate endpoints do not expose the full per-field price
  table; for those fields, say the exact maximum is unavailable through the
  API and do not present a flat-rate guess as a ceiling. Record the job's
  reservation and actual charge after settlement.
- Default to **20 places** if the user gives no number. If the user asks for
  all matches, use the count to set an explicit list import limit (subject to
  the 10,000-row cap) and explain the resulting cost before submitting.

## Workflow

### 1. Resolve the geography (free)

```bash
curl -s "https://api.voygr.tech/v1/geo/suggest?q=Austin%20TX&limit=5" -H "X-API-Key: $VOYGR_API_KEY"
```

Use the returned `geography_id` (e.g. `city:TX:austin`). Ask the user if the
match is ambiguous. Prefer a city, ZIP, or state geography ID to a hand-drawn
bounding box; a box can be much wider than the place the user named, and the
free preview does not accept boxes. Do not construct an ID by replacing spaces
in a place name with underscores. Check suggested IDs with free count and
preview calls before a paid search. A plausible label or bounding box alone
does not establish that the geography contains the expected places.

### 2. Pick categories (free)

```bash
curl -s https://api.voygr.tech/v1/places/categories -H "X-API-Key: $VOYGR_API_KEY"
```

`categories` filters taxonomy tags such as `shop=jewelry`.
`categories_any_level` filters category-path names such as `gay_bar`; a parent
such as `bar` also matches its children. These filters are different and are
ANDed if both are sent. For a category-path request, use
`categories_any_level` in count, preview, search, and search-backed list
creation. Do not infer that the API lacks a category because the other filter
returns zero. If the category is unclear, compare free counts and previews
before any paid search; `q` matches place names, not category paths.

### 3. Size the query before spending (free)

```bash
curl -s -X POST https://api.voygr.tech/v1/places/count -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"geography_id":"city:TX:austin","categories":["shop=jewelry"],"independents_only":true}'
```

`independents_only: true` hides likely national chains. It is a
name-frequency heuristic and can also hide independent places.
Read `capped` and `count_is_estimate` before calling a count exact. Preview
the same filter for free to inspect five matching places. For a category-path
search, use the same `categories_any_level` body in both calls:

```bash
curl -s -X POST https://api.voygr.tech/v1/places/count -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"geography_id":"city:NY:new york","categories_any_level":["gay_bar"]}'
```

```bash
curl -s -X POST https://api.voygr.tech/v1/places/preview -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"geography_id":"city:NY:new york","categories_any_level":["gay_bar"]}'
```

Preview has no pagination. In the live NYC test, `city:NY:new york` returned
63 `gay_bar` matches, while `city:NY:new_york` was rejected as
`UNKNOWN_GEOGRAPHY`. The suggested `city:NY:new york city` returned zero for
the same filter, and the `city:NY:new york` bounding box was unusually wide;
verify geography scope from the returned places before claiming citywide
coverage. If the user needs search results before creating a list,
`/v1/places/search` is paid. After approval, use the same filter with a
specific limit:

```bash
curl -s -X POST https://api.voygr.tech/v1/places/search -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"geography_id":"city:NY:new york","categories_any_level":["gay_bar"],"limit":20}'
```

Follow `next_cursor` until null or the approved total limit, and account for
search charges separately from a later list import. Otherwise create the list
directly from the approved search filter. Report the count and scope.

### 4. Turn the user's question into fields (free)

```bash
curl -s -X POST https://api.voygr.tech/v1/fields/suggest -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"goal":"owner name and email, and whether they sell lab-grown diamonds"}'
```

Review the proposed field specs against the user's request and the built-in
field catalog; do not replace a precise `owners` field with a vague custom
owner question. Anything listed as unsupported cannot be delivered; tell the
user instead of trying.

### 5. Save the places as a list (paid: per place imported)

```bash
curl -s -X POST https://api.voygr.tech/v1/lists -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Austin jewelers","search":{"geography_id":"city:TX:austin","categories":["shop=jewelry"],"independents_only":true,"limit":20}}'
```

Keep the returned `list_id`. A user's own CSV can be used instead of a
search (`POST /v1/lists/upload-url` with `filename`, multipart POST the CSV to
the returned `url` with every returned `fields` entry, then `POST /v1/lists`
with the returned `key` as `upload_key`). The presigned URL can be on a
different host; send no `X-API-Key` header there. Read the list and row count
before filling. For a category-path list, use `categories_any_level` inside
`search`, exactly as in count and preview.

### 6. Fill the fields (paid: per completed lookup)

```bash
curl -s -X POST https://api.voygr.tech/v1/jobs/deep-research -H "X-API-Key: $VOYGR_API_KEY" \
  -H "Content-Type: application/json" -H "Idempotency-Key: <job-key>" \
  -d '{"list_id":"<list_id>","row_count":20,"fields":[
        {"name":"owners","include":["email","phone"]},
        {"name":"lab_grown_diamonds","description":"whether this jeweler sells lab-grown diamonds","value_type":"bool"}]}'
```

- `row_count` must equal the number of rows targeted (the list size, or the
  length of `row_ids`).
- `owners` returns the individual owner(s) with names and roles plus any
  contacts in `include`. Contact prices differ; do not treat each as one
  credit. An unknown owner or contact is not proof the person does not exist.
  `owner_org` covers businesses owned by a company; `key_people` covers
  leadership beyond the owner.
- Custom fields: give a short `name`, a one-sentence `description`, and a
  `value_type` (`bool`, `enum` with `allowed_values`, `string`, `number`).
- The reserve is `row_count x the sum of the requested field prices` (including
  people contact units), multiplied by the account's fill rate. A completed
  lookup that abstains can be charged; a failed lookup is free. Read the job's
  reservation and settled charge rather than inferring them from filled cells.
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

Also poll `GET /v1/jobs/<batch_id>` for `completed`, `failed`, or `cancelled`
and compare `GET /v1/usage` before and after settlement. A cancellation
response does not by itself prove the credit reservation was released.

Export the whole list as CSV when done:

```bash
curl -s "https://api.voygr.tech/v1/lists/<list_id>/export" -H "X-API-Key: $VOYGR_API_KEY" -o leads.csv
```

Inspect CSV headers and values before describing its shape. Some nested values,
including owners and contacts, may appear as JSON in a CSV cell rather than
separate columns.

## Presenting results

Summarize as a table: place, address, the requested fields. Distinguish a
returned value, an abstention, a failed lookup, and an unprocessed cell. Show
the actual charge and any remaining reservation after checking job status and
usage. Offer the CSV path.

## Errors

- `402`: out of credits. Tell the user to top up in the app.
- `403`: the key lacks access to prospecting; the user should sign in once at
  https://app.voygr.tech with the same email (adds prospecting to the key).
- `400` with a message: show the message; usually a bad geography, category
  or `row_count` mismatch.
- Places outside the US are not covered.
