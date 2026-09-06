#!/usr/bin/env python3
"""Conservative, private-state skill synchronization (Python 3.10+, git, gitleaks).

Config (all filesystem paths except catalog must be absolute):
{"version":1,"remote":"/absolute/bare.git","branch":"main",
 "workspace":"/absolute/dotfiles","cache_dir":"/absolute/private-cache",
 "scanner":"/absolute/gitleaks","mappings":[
 {"catalog":"skills/example","targets":["/absolute/hermes/example",
 "/absolute/codex/example","/absolute/opencode/example"]}]}

The config must be a private regular file (0600). A pending.json journal blocks
all later runs after a partial transaction; reconcile its backups, remote and
installations manually before removing it. Never remove it simply to retry.
Rejected pushes block safely; there is no automatic rebase/retry. Excluded local
files are never copied or deleted. Missing whole skills and symlinks block.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from urllib.parse import urlsplit


class Blocked(RuntimeError):
    pass


def run(args, *, cwd=None, accepted=(0,), env=None):
    try:
        p = subprocess.run([str(a) for a in args], cwd=cwd, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    except subprocess.TimeoutExpired:
        raise Blocked(f"{Path(str(args[0])).name} timed out after 120 seconds") from None
    if p.returncode not in accepted:
        # Do not print command output: scanner/git output can contain secrets.
        raise Blocked(f"{Path(str(args[0])).name} failed (exit {p.returncode}); output withheld")
    return p


def git(repo, *args, accepted=(0,)):
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("GIT_"):
            env.pop(k)
    env.update(GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1",
               GIT_CONFIG_GLOBAL=os.devnull)
    return run(["git", "-c", "core.hooksPath=" + os.devnull,
                "-c", "core.autocrlf=false", "-c", "commit.gpgSign=false",
                "-c", "core.fsmonitor=false", *args], cwd=repo, accepted=accepted, env=env)


def atomic(path, data, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".skill-sync-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            os.fchmod(f.fileno(), mode)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        d = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(d)
        finally:
            os.close(d)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def json_write(path, obj):
    atomic(path, (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode())


def no_symlinks(path):
    p = Path(path)
    for item in (p, *p.parents):
        if item.is_symlink():
            raise Blocked(f"symlink path forbidden: {item}")


def absolute(value):
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise Blocked("filesystem paths must be absolute")
    p = Path(os.path.abspath(value))
    no_symlinks(p)
    return p


def overlaps(a, b):
    return a == b or a in b.parents or b in a.parents


def config_load(path):
    path = absolute(str(Path(path).absolute()))
    if not path.is_file() or path.stat().st_mode & 0o077:
        raise Blocked("config must be a private regular file (chmod 600)")
    c = json.loads(path.read_text())
    required = {"version", "remote", "branch", "workspace", "cache_dir", "scanner", "mappings"}
    if set(c) != required or c["version"] != 1:
        raise Blocked("unsupported config schema")
    for k in ("workspace", "cache_dir", "scanner"):
        c[k] = absolute(c[k])
    if not isinstance(c["remote"], str) or not re.match(r"^(?:/|https://|ssh://|[\w.-]+@[\w.-]+:)", c["remote"]):
        raise Blocked("remote must be an absolute local path, HTTPS or SSH URL")
    if not isinstance(c["branch"], str):
        raise Blocked("branch must be a string")
    if "://" in c["remote"]:
        url = urlsplit(c["remote"])
        if url.password or url.query or url.fragment or (url.scheme == "https" and url.username):
            raise Blocked("credentials/query/fragment forbidden in remote URL")
    git(None, "check-ref-format", "refs/heads/" + c["branch"])
    if not c["mappings"]:
        raise Blocked("at least one mapping required")
    catalogs, targets = [], []
    for m in c["mappings"]:
        if set(m) != {"catalog", "targets"} or not isinstance(m["catalog"], str):
            raise Blocked("invalid mapping")
        p = PurePosixPath(m["catalog"])
        if p.is_absolute() or ".." in p.parts or not p.parts or any(x.startswith(".") for x in p.parts) or str(p) != m["catalog"]:
            raise Blocked("invalid catalog path")
        if not isinstance(m["targets"], list) or not m["targets"]:
            raise Blocked("mapping needs targets")
        m["targets"] = [absolute(x) for x in m["targets"]]
        catalogs.append(Path(m["catalog"]))
        targets.extend(m["targets"])
    for paths in (catalogs, targets):
        for i, a in enumerate(paths):
            if any(overlaps(a, b) for b in paths[i + 1:]):
                raise Blocked("overlapping or duplicate mappings")
    for t in targets:
        if overlaps(t, c["workspace"]) or overlaps(t, c["cache_dir"]):
            raise Blocked("installations must be outside workspace and cache")
    if overlaps(c["cache_dir"], c["workspace"]):
        raise Blocked("cache must be outside working checkout")
    return c


# Deliberately narrow: arbitrary executable/binary assets are not imported.
EXTENSIONS = {".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml", ".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".ts", ".css", ".html", ".svg", ".csv"}
DENIED = {"node_modules", "__pycache__", "cache", "caches", "venv", "env", "dist", "build", "credentials", "secrets", "private", "token", "tokens", "logs", "backups", "archives", "models", "outputs", "browser-state"}


def allowed(name):
    parts = PurePosixPath(name).parts
    if any(p.startswith(".") or p.lower() in DENIED for p in parts):
        return False
    leaf = parts[-1].lower()
    source = Path(leaf).suffix in {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".ts"}
    if not source and any(s in leaf for s in ("credential", "secret", "token", "password", "id_rsa", "id_ed25519")):
        return False
    return Path(leaf).suffix in EXTENSIONS or leaf in {"license", "notice", "makefile"}


def snapshot(root, strict=False, excluded=None):
    no_symlinks(root)
    if not root.exists():
        return None
    if not root.is_dir():
        raise Blocked(f"skill is not a directory: {root}")
    result = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            p = Path(parent) / name
            if p.is_symlink():
                raise Blocked(f"symlink in skill: {p}")
        denied_dirs = [d for d in dirs if d.startswith(".") or d.lower() in DENIED]
        if strict and denied_dirs:
            raise Blocked(f"disallowed remote managed directory: {Path(parent) / denied_dirs[0]}")
        if excluded is not None:
            excluded.extend(str(Path(parent) / d) + "/" for d in denied_dirs)
        dirs[:] = [d for d in dirs if d not in denied_dirs]
        for name in files:
            p = Path(parent) / name
            rel = p.relative_to(root).as_posix()
            if not allowed(rel):
                if strict:
                    raise Blocked(f"disallowed remote managed file: {p}")
                if excluded is not None:
                    excluded.append(str(p))
                continue
            if not stat.S_ISREG(p.stat().st_mode):
                raise Blocked("non-regular skill file")
            result[rel] = p.read_bytes()
    return result


def encode(snap):
    return None if snap is None else {k: base64.b64encode(v).decode() for k, v in sorted(snap.items())}


def decode(snap):
    return None if snap is None else {k: base64.b64decode(v, validate=True) for k, v in snap.items()}


def workspace_check(c):
    w = c["workspace"]
    if Path(git(w, "rev-parse", "--show-toplevel").stdout.decode().strip()).resolve() != w.resolve():
        raise Blocked("workspace must be the checkout root")
    paths = [m["catalog"] for m in c["mappings"]]
    if git(w, "status", "--porcelain", "--untracked-files=all", "--", *paths).stdout:
        raise Blocked("working checkout has dirty managed paths")
    # Compare directly with configured remote tip, not possibly stale tracking refs.
    head = git(w, "ls-remote", "--exit-code", c["remote"], "refs/heads/" + c["branch"]).stdout.decode().split()
    if not head:
        raise Blocked("remote branch missing")
    oid = head[0]
    # No fetch into the user's checkout. Missing remote objects means fail closed.
    if git(w, "cat-file", "-e", oid + "^{commit}", accepted=(0, 1, 128)).returncode:
        # Locally outgoing commits can still be proven absent if HEAD is an ancestor
        # of remote (done in the dedicated clone below).
        return git(w, "rev-parse", "HEAD").stdout.decode().strip()
    if git(w, "log", "--format=%H", oid + "..HEAD", "--", *paths).stdout:
        raise Blocked("working checkout has outgoing commits touching managed paths")
    return git(w, "rev-parse", "HEAD").stdout.decode().strip()


def merge_versions(base, versions, scratch):
    changed = []
    for v in versions:
        if v != base and v not in changed:
            changed.append(v)
    if not changed:
        return base
    if len(changed) == 1:
        return changed[0]
    if base is None or any(v is None for v in changed):
        raise Blocked("add/add or delete/modify conflict")
    for v in [base, *changed]:
        try:
            v.decode("utf-8")
        except UnicodeDecodeError:
            raise Blocked("binary conflict") from None
        if b"\0" in v:
            raise Blocked("binary conflict")
    # Pairwise merges against the SAME base. Deterministic order: remote, then
    # targets in config order. git merge-file detects overlapping text edits.
    current = changed[0]
    for other in changed[1:]:
        for name, content in (("ours", current), ("base", base), ("theirs", other)):
            atomic(scratch / name, content)
        p = git(None, "merge-file", "-p", str(scratch / "ours"), str(scratch / "base"), str(scratch / "theirs"), accepted=tuple(range(256)))
        if p.returncode:
            raise Blocked("overlapping text conflict")
        current = p.stdout
    return current


def scanner(c, repo, tree, start):
    exe = c["scanner"]
    if not exe.is_file() or not os.access(exe, os.X_OK):
        raise Blocked("mandatory gitleaks executable unavailable")
    # Force scanner execution away from checkout config, and reject repository
    # policy files rather than letting public content weaken local scan policy.
    if any(p.name in {".gitleaks.toml", ".gitleaksignore"} for p in tree.rglob("*")):
        raise Blocked("repository gitleaks overrides forbidden")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GITLEAKS_") and not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    ignore = c["cache_dir"] / "empty-gitleaks-ignore"
    atomic(ignore, b"")
    policy = c["cache_dir"] / "trusted-gitleaks.toml"
    atomic(policy, b"[extend]\nuseDefault = true\n")
    common = ["--redact", "--no-banner", "--config", str(policy), "--ignore-gitleaks-allow", "--gitleaks-ignore-path", str(ignore)]
    for kind, source, extra in (("dir", tree, []), ("git", repo, ["--log-opts=" + start + "..HEAD"])):
        report = c["cache_dir"] / ("scan-" + kind + ".json")
        if report.exists():
            report.unlink()
        p = run([exe, kind, *common, *extra, "--report-format=json", "--report-path", str(report), str(source)], cwd=c["cache_dir"], env=env, accepted=tuple(range(256)))
        if not report.is_file():
            raise Blocked(f"gitleaks {kind}: missing mandatory JSON report (exit {p.returncode})")
        findings = json.loads(report.read_text())
        if not isinstance(findings, list):
            raise Blocked(f"gitleaks {kind}: malformed report")
        if findings:
            details = []
            for f in findings:
                # Only category/location, NEVER Secret, Match, or line content.
                details.append(str(f.get("RuleID", "unknown")) + " at " + str(f.get("File", "unknown")) + ":" + str(f.get("StartLine", "?")))
            raise Blocked(f"gitleaks {kind}: {len(findings)} finding(s): " + "; ".join(details[:20]))
        if p.returncode:
            raise Blocked(f"gitleaks {kind} failed closed (exit {p.returncode})")


def sync(c, apply):
    cache = c["cache_dir"]
    cache.mkdir(parents=True, mode=0o700, exist_ok=True)
    if cache.stat().st_mode & 0o077:
        raise Blocked("cache must be private (chmod 700)")
    with (cache / "lock").open("a+b") as lock:
        os.chmod(cache / "lock", 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Blocked("another sync holds the lock") from None
        return locked_sync(c, apply)


def locked_sync(c, apply):
    cache = c["cache_dir"]
    pending = cache / "pending.json"
    if pending.exists():
        raise Blocked("interrupted transaction: inspect pending.json and backups; manual recovery required")
    identity = hashlib.sha256(json.dumps({k: c[k] for k in ("remote", "branch", "workspace")}, sort_keys=True, default=str).encode()).hexdigest()
    state_path = cache / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"identity": identity, "bases": {}}
    if state["identity"] != identity:
        raise Blocked("config changed: use a new cache or explicitly migrate private state")
    if state_path.exists():
        actual = {catalog: {name: hashlib.sha256(data).hexdigest() for name, data in (decode(snap) or {}).items()} for catalog, snap in state["bases"].items()}
        if actual != state.get("hashes") or not re.fullmatch(r"[0-9a-f]{40,64}", state.get("remote_commit", "")):
            raise Blocked("private state hashes/commit missing or corrupt; manual recovery required")
    workspace_head = workspace_check(c)
    repo = cache / "clone"
    no_symlinks(repo)
    if not repo.exists():
        git(None, "clone", "--no-checkout", "--origin", "origin", "--", c["remote"], str(repo))
    if git(repo, "remote", "get-url", "origin").stdout.decode().strip() != c["remote"]:
        raise Blocked("cache clone remote mismatch")
    git(repo, "fetch", "--no-tags", "origin", "refs/heads/" + c["branch"])
    start = git(repo, "rev-parse", "FETCH_HEAD").stdout.decode().strip()
    # Fetch the checkout's HEAD read-only into the private clone to inspect all
    # commits not on the configured branch (also works after remote advanced).
    git(repo, "fetch", "--no-tags", str(c["workspace"]), workspace_head)
    if git(repo, "log", "--format=%H", start + "..FETCH_HEAD", "--", *[m["catalog"] for m in c["mappings"]]).stdout:
        raise Blocked("working checkout has outgoing commits touching managed paths")
    git(repo, "checkout", "--detach", "--force", start)
    git(repo, "clean", "-fdx")  # dedicated disposable clone only
    plans, bases, conflicts, modes, excluded = [], dict(state["bases"]), [], dict(state.get("modes", {})), []
    participants = state.get("participants", {})
    with tempfile.TemporaryDirectory(prefix="proposal-", dir=cache) as tmp:
        tree = Path(tmp) / "tree"
        tree.mkdir()
        # Build exactly the tracked proposed tree; never copy .git or run files.
        tracked = git(repo, "ls-files", "--stage", "-z").stdout.split(b"\0")
        for entry in tracked:
            if not entry:
                continue
            meta, raw = entry.split(b"\t", 1)
            mode = meta.split()[0]
            name = os.fsdecode(raw)
            if not any(name == m["catalog"] or name.startswith(m["catalog"] + "/") for m in c["mappings"]):
                continue
            if mode not in (b"100644", b"100755"):
                raise Blocked("symlinks/submodules in remote tree are forbidden")
            dest = tree / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo / name, dest)
        scratch = Path(tmp) / "merge"
        scratch.mkdir()
        for m in c["mappings"]:
            catalog = m["catalog"]
            remote = snapshot(tree / catalog, strict=True)
            local = [snapshot(t, excluded=excluded) for t in m["targets"]]
            base = decode(state["bases"].get(catalog))
            known = set(participants.get(catalog, []))
            # New selections may be absent; previously participating skills may not.
            if (remote is None and base is not None) or any(s is None and str(t) in known for t, s in zip(m["targets"], local)):
                conflicts.append({"catalog": catalog, "reason": "entire skill missing", "base": encode(base), "remote": encode(remote), "targets": [{"path": str(t), "files": encode(s)} for t, s in zip(m["targets"], local)]})
                continue
            remote = remote or {}
            original_local = local
            local = [s or {} for s in local]
            result = {}
            before = len(conflicts)
            for name in sorted(set(base or {}) | set(remote) | set().union(*(set(s) for s in local))):
                b = (base or {}).get(name)
                versions = [remote.get(name), *[s.get(name) for t, s in zip(m["targets"], local) if str(t) in known or name in s]]
                # Before the first base exists, absence is not a deletion.
                if base is None:
                    versions = [v for v in versions if v is not None]
                try:
                    merged = merge_versions(b, versions, scratch)
                    if merged is not None:
                        result[name] = merged
                except Blocked as e:
                    conflicts.append({"catalog": catalog, "file": name, "reason": str(e), "base": encode({name: b}) if b is not None else None, "remote": encode({name: remote[name]}) if name in remote else None, "targets": [{"path": str(t), "files": encode({name: s[name]}) if name in s else None} for t, s in zip(m["targets"], local)]})
            if len(conflicts) != before:
                continue
            if "SKILL.md" not in result:
                conflicts.append({"catalog": catalog, "reason": "proposal lacks SKILL.md", "base": encode(base), "remote": encode(remote), "targets": [{"path": str(t), "files": encode(s)} for t, s in zip(m["targets"], local)]})
                continue
            # File/directory collisions must be rejected before touching sources.
            for name in result:
                if any(str(p) in result for p in PurePosixPath(name).parents if str(p) != "."):
                    raise Blocked("file/directory collision in proposal")
            bases[catalog] = encode(result)
            modes[catalog] = {}
            for name in result:
                sources = [repo / catalog / name, *[t / name for t in m["targets"]]]
                bits = [bool(p.stat().st_mode & 0o111) for p in sources if p.is_file()]
                old_mode = state.get("modes", {}).get(catalog, {}).get(name)
                if old_mode is None:
                    executable = any(bits)
                else:
                    old_bit = bool(old_mode & 0o111)
                    executable = next((bit for bit in bits if bit != old_bit), old_bit)
                modes[catalog][name] = 0o755 if executable else 0o644
            plans.append((m, remote, original_local, result))
        if conflicts:
            location = cache / "conflicts" / (uuid.uuid4().hex + ".json")
            if apply:
                json_write(location, conflicts)
            details = "; ".join(x["catalog"] + "/" + x.get("file", "") + ": " + x["reason"] for x in conflicts)
            raise Blocked(f"{len(conflicts)} conflict(s); no installations changed; " + details + ("; versions saved privately at " + str(location) if apply else " (dry-run: no conflict state written)"))
        changes = []
        for m, remote, local, result in plans:
            for name in sorted(set(remote) | set(result)):
                if remote.get(name) != result.get(name) or (name in result and bool((repo / m["catalog"] / name).stat().st_mode & 0o111) != bool(modes[m["catalog"]][name] & 0o111)):
                    changes.append(m["catalog"] + "/" + name)
                    put(tree / m["catalog"] / name, result.get(name), modes[m["catalog"]].get(name))
        # Mirror only explicit changed paths to clone, then stage only those paths.
        for name in changes:
            put(repo / name, (tree / name).read_bytes() if (tree / name).exists() else None, stat.S_IMODE((tree / name).stat().st_mode) if (tree / name).exists() else None)
        if changes:
            # Scan the candidate BEFORE creating a commit, then scan the outgoing
            # commit itself below. Both gates must pass before any public write.
            scanner(c, repo, tree, start)
            git(repo, "add", "--", *changes)
            git(repo, "-c", "user.name=Skill Sync", "-c", "user.email=skill-sync@localhost", "commit", "-m", "Sync managed agent skills")
        # Mandatory even for local-only deployment and unchanged runs; fail closed.
        scanner(c, repo, tree, start)
        deploy = any(s != result or any(bool((t / n).stat().st_mode & 0o111) != bool(modes[m["catalog"]][n] & 0o111) for n in result) for m, _, locals_, result in plans for t, s in zip(m["targets"], locals_))
        new_participants = {m["catalog"]: sorted({str(t) for t in m["targets"]}) for m in c["mappings"]}
        state_changed = state["bases"] != bases or participants != new_participants
        if not changes and not deploy and not state_changed:
            return
        if not apply:
            print("dry-run: verified proposal; " + str(len(changes)) + " catalog file change(s); deployment=" + str(deploy).lower() + f"; excluded local entries={len(excluded)}")
            return
        # Recheck ALL sources before beginning a write transaction.
        workspace_check(c)
        for m, _, local, _ in plans:
            for target, original in zip(m["targets"], local):
                if snapshot(target) != original:
                    raise Blocked("installation changed during planning; retry")
        txn = uuid.uuid4().hex
        backup = cache / "backups" / txn
        backup.mkdir(parents=True, mode=0o700)
        saved = [{"catalog": m["catalog"], "targets": [{"path": str(t), "files": encode(s), "modes": {n: stat.S_IMODE((t / n).stat().st_mode) for n in (s or {})}} for t, s in zip(m["targets"], local)], "proposed": encode(result), "proposed_modes": modes[m["catalog"]]} for m, _, local, result in plans]
        json_write(backup / "versions.json", saved)
        journal = {"transaction": txn, "phase": "prepared", "remote_before": start, "commit": git(repo, "rev-parse", "HEAD").stdout.decode().strip(), "backup": str(backup), "identity": identity, "excluded": excluded}
        json_write(pending, journal)
        if changes:
            # No force, no automatic retry: rejected push retains local edits and
            # journal. Manual inspection is necessary if transport result ambiguous.
            git(repo, "push", "origin", "HEAD:refs/heads/" + c["branch"])
        tip = git(repo, "ls-remote", "--exit-code", "origin", "refs/heads/" + c["branch"]).stdout.decode().split()[0]
        if tip != journal["commit"]:
            raise Blocked("remote changed before deployment; pending recovery required")
        journal["phase"] = "deploying"
        json_write(pending, journal)
        for m, _, local, result in plans:
            for target, original in zip(m["targets"], local):
                if snapshot(target) != original:
                    raise Blocked("concurrent installation edit; pending recovery required")
                original = original or {}
                target.mkdir(parents=True, exist_ok=True)
                for name in sorted(set(original) | set(result)):
                    if original.get(name) == result.get(name) and (name not in result or bool((target / name).stat().st_mode & 0o111) == bool(modes[m["catalog"]][name] & 0o111)):
                        continue
                    p = target / name
                    no_symlinks(p)
                    current = p.read_bytes() if p.is_file() else None
                    if current != original.get(name):
                        raise Blocked("concurrent file edit; pending recovery required")
                    put(p, result.get(name), modes[m["catalog"]].get(name))
                if snapshot(target) != result:
                    raise Blocked("deployment recheck failed; pending recovery required")
        # Recheck every installation together before committing the new base.
        for m, _, _, result in plans:
            if any(snapshot(t) != result for t in m["targets"]):
                raise Blocked("post-deployment concurrent edit; pending recovery required")
        json_write(state_path, {"identity": identity, "bases": bases, "participants": new_participants, "remote_commit": journal["commit"], "hashes": {catalog: {n: hashlib.sha256(data).hexdigest() for n, data in (decode(s) or {}).items()} for catalog, s in bases.items()}, "modes": modes})
        pending.unlink()
        print("synced: " + str(len(changes)) + f" catalog file change(s); installations verified; excluded local entries={len(excluded)}")


def put(path, content, mode=None):
    no_symlinks(path)
    if content is None:
        if path.exists():
            path.unlink()
    else:
        mode = mode if mode is not None else (stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644)
        atomic(path, content, mode)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    os.umask(0o077)
    try:
        sync(config_load(args.config), args.apply)
    except (Blocked, OSError, ValueError, KeyError, TypeError) as e:
        print("skill-sync blocked: " + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
