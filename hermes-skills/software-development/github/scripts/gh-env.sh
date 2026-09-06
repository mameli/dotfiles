#!/usr/bin/env bash
# Source this file using its installed absolute path (Bash required).
# Read-only GitHub.com auth/repo detection; needs python3, git, and gh or curl.
# Sets GH_AUTH_METHOD (gh/curl/none), GITHUB_TOKEN, GH_USER,
# GH_OWNER, GH_REPO, GH_OWNER_REPO. Never prints credentials.
# Refuse tracing rather than exposing secrets or altering the caller's options.
case $- in *x*) printf '%s\n' 'Disable shell tracing before loading GitHub auth.' >&2; return 1 2>/dev/null || exit 1 ;; esac

_github_skill_scripts=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
GH_AUTH_METHOD=none
GITHUB_TOKEN=${GH_TOKEN:-${GITHUB_TOKEN:-}}
GH_USER=
GH_OWNER=
GH_REPO=
GH_OWNER_REPO=

if command -v gh >/dev/null 2>&1 && gh auth status --hostname github.com >/dev/null 2>&1; then
    GH_USER=$(gh api --hostname github.com user --jq '.login' 2>/dev/null) || GH_USER=
    if [ -n "$GH_USER" ]; then GH_AUTH_METHOD=gh; fi
fi

if [ "$GH_AUTH_METHOD" = none ]; then
    if [ -z "$GITHUB_TOKEN" ]; then
        # Read only the selected profile's .env; never execute it as shell code.
        GITHUB_TOKEN=$(python3 - "${HERMES_HOME:-$HOME/.hermes}/.env" <<'PY'
import pathlib, re, sys
try:
    lines = pathlib.Path(sys.argv[1]).read_text().splitlines()
except (OSError, UnicodeError):
    lines = []
for line in lines:
    match = re.match(r'^\s*(?:export\s+)?GITHUB_TOKEN\s*=\s*(.*)$', line)
    if not match:
        continue
    value = match[1].strip()
    if value.startswith(('"', "'")):
        quote = value[0]
        end = value.find(quote, 1)
        if end < 0 or (value[end+1:].strip() and not value[end+1:].lstrip().startswith('#')):
            continue
        value = value[1:end]
    else:
        value = re.split(r'\s+#', value, maxsplit=1)[0].strip()
    if value and not any(ord(c) <= 32 or ord(c) == 127 for c in value):
        print(value)
        break
PY
        ) || GITHUB_TOKEN=
    fi
    if [ -z "$GITHUB_TOKEN" ] && [ -f "$HOME/.git-credentials" ]; then
        GITHUB_TOKEN=$(python3 "$_github_skill_scripts/git-credential-token.py" "$HOME/.git-credentials") || GITHUB_TOKEN=
    fi
    # Reject newline/control injection before passing the header over stdin.
    if [ -n "$GITHUB_TOKEN" ] && [[ ! "$GITHUB_TOKEN" =~ [[:space:][:cntrl:]] ]]; then
        GH_USER=$(printf 'Authorization: Bearer %s\n' "$GITHUB_TOKEN" |
            curl --fail --silent --show-error --connect-timeout 10 --max-time 20 \
                --header @- https://api.github.com/user 2>/dev/null |
            python3 -c 'import json,sys; print(json.load(sys.stdin).get("login", ""))' 2>/dev/null) || GH_USER=
        if [ -n "$GH_USER" ]; then GH_AUTH_METHOD=curl; fi
    fi
fi

_remote_url=$(git remote get-url origin 2>/dev/null) || _remote_url=
# Match the host exactly; never mistake github.com.evil or a path for GitHub.
if [[ "$_remote_url" =~ ^(https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/]+)/([^/]+)$ ]]; then
    GH_OWNER=${BASH_REMATCH[2]}
    GH_REPO=${BASH_REMATCH[3]%.git}
    GH_OWNER_REPO=$GH_OWNER/$GH_REPO
fi
unset _remote_url _github_skill_scripts
printf 'GitHub Auth: %s\n' "$GH_AUTH_METHOD"
if [ -n "$GH_USER" ]; then printf 'User: %s\n' "$GH_USER"; fi
if [ -n "$GH_OWNER_REPO" ]; then printf 'Repo: %s\n' "$GH_OWNER_REPO"; fi
if [ "$GH_AUTH_METHOD" = none ]; then printf '%s\n' 'Not authenticated — read references/auth.md in the github skill.'; fi
export GH_AUTH_METHOD GITHUB_TOKEN GH_USER GH_OWNER GH_REPO GH_OWNER_REPO
