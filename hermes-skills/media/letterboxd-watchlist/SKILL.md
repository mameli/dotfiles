---
name: letterboxd-watchlist
description: Use when adding films to a Letterboxd watchlist.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [letterboxd, films, watchlist, browser, cdp]
---

# Letterboxd Watchlist

Use this skill when the user asks to add one or more films to their Letterboxd watchlist. Derive the account from the authenticated profile menu or settings page, never from a fixed username or a public film page. If the account is unclear or differs from the one requested, ask before changing its watchlist.

## Browser lane

Use the dedicated persistent Google Chrome profile:

- CDP endpoint: `${SKILLS_CDP_URL}`
- Chrome user-data-dir: `${SKILLS_BROWSER_USER_DATA_DIR}`
- Chrome profile directory: `${SKILLS_BROWSER_PROFILE}`
- LaunchAgent label: `${SKILLS_BROWSER_LAUNCH_AGENT}`
- Hermes config: `browser.use_real_profile = false`, `browser.cdp_url = ${SKILLS_CDP_URL}`

Call `browser_exec` **without** `local=true`; reuse `session="letterboxd"` for related requests.

If CDP is unavailable, inspect readiness first. Only after the user authorizes a possible interruption, restart the configured dedicated browser and wait for readiness; never infer a service label:

```bash
if [ -n "${SKILLS_BROWSER_LAUNCH_AGENT:-}" ]; then
  launchctl kickstart -k "gui/$(id -u)/${SKILLS_BROWSER_LAUNCH_AGENT}"
else
  printf '%s\n' 'No LaunchAgent configured; ask how the existing browser is managed. Do not guess a service.' >&2
fi
for i in {1..20}; do
  curl -fsS "${SKILLS_CDP_URL:-http://127.0.0.1:9222}/json/version" >/dev/null && break
  sleep 1
done
curl -fsS "${SKILLS_CDP_URL:-http://127.0.0.1:9222}/json/version" >/dev/null || {
  printf '%s\n' 'CDP unavailable; resolve browser readiness before continuing.' >&2
  false
}
```

Do not request, receive, or type the user's password, passkey, OTP, or 2FA code. If authentication has expired, open `https://letterboxd.com/settings/`, ask the user to sign in manually in the dedicated Chrome window, and continue only after they confirm.

## Workflow

### 1. Resolve the exact film

- Prefer a canonical Letterboxd film URL supplied by the user.
- Otherwise search Letterboxd or the web by title, adding the year/director when known.
- Before changing anything, verify the canonical film page's displayed title, year, and—when useful—director.
- Never silently choose among remakes, duplicate titles, alternate cuts, or similarly named films. If the title alone is genuinely ambiguous, ask the user which year/version they mean.
- Preserve the user's title exactly during lookup; do not “correct” it into a different film.

### 2. Check authentication

A film page alone may be public, so absence of a login wall is not sufficient proof. The watchlist control should reflect the authenticated account. When uncertain, navigate to `https://letterboxd.com/settings/`:

- authenticated: settings page remains accessible;
- unauthenticated: it redirects or renders “Sign in to Letterboxd”.

### 3. Inspect before clicking

On the verified canonical film page, inspect the watchlist action:

```js
document.querySelector(
  'a.add-to-watchlist, a.remove-from-watchlist, a.action.-watchlist'
)
```

Interpret the class/state:

- `remove-from-watchlist` or text such as “This film is in your Watchlist” → **already present**;
- `add-to-watchlist` or an inactive `action -watchlist` → **not present**.

The control is a toggle. **Never click it when the film is already present**, because that removes the film.

### 4. Add only when absent

After exact-film and authentication checks, click only an add-state control:

```js
(() => {
  const action = document.querySelector(
    'a.add-to-watchlist, a.action.-watchlist:not(.remove-from-watchlist)'
  );
  if (!action) return false;
  action.click();
  return true;
})()
```

Wait briefly for Letterboxd's request and DOM update.

### 5. Verify the external state

Re-read the same film page control. Success requires both:

- class contains `remove-from-watchlist`; and
- visible state says the film is in the watchlist, or the equivalent active watchlist state is present.

A successful click or tool return alone is not proof. If the control does not transition, reload once and inspect again. Do not retry a click blindly: first determine whether the first click actually succeeded.

For multiple films, process every requested title independently and preserve a per-film result: `added`, `already present`, `ambiguous`, or `failed`.

## Response style

Reply briefly in the user's language:

- added: `Aggiunto **Titolo (anno)** alla watchlist. Verificato: ora risulta presente.`
- already present: `**Titolo (anno)** era già nella watchlist; non ho cliccato per evitare di rimuoverlo.`
- ambiguous: list the smallest useful set of candidate years/directors and ask which one.
- failed: state the concrete blocker without claiming the list changed.

Do not narrate browser steps or expose cookies/session data.

## Local environment

Read the relevant exported variables; if unavailable, source `${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills/env.zsh` into the command environment. Never print credential values. In prose and configuration examples, `${VAR}` denotes a value to resolve; do not write literal placeholders into application settings.

Browser workflow values use explicit task settings > nonempty environment > generic defaults: `SKILLS_CDP_URL` defaults to `http://127.0.0.1:9222`, `SKILLS_BROWSER_PROFILE` to `Default`. `SKILLS_BROWSER_USER_DATA_DIR` identifies the existing profile root; if needed but unset, ask rather than invent a path. Optional `SKILLS_BROWSER_LAUNCH_AGENT` and `SKILLS_BROWSER_LOG_DIR` select the macOS service and diagnostic logs; unset means skip those operations. The shell examples consume the endpoint/service values; profile and log values are workflow inputs. These settings do not provision Chrome or automatically reconfigure Hermes. Verify the configured `browser.cdp_url` matches the selected endpoint.
