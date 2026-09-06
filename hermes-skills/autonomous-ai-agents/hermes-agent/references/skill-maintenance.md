# Installed-skill maintenance

Scope changes to the active profile and the skills implicated by the request. Prefer a short trigger description and a root router over a large multi-workflow body; keep task-specific constraints, helpers, and failure-recovery knowledge in the relevant reference. Do not add generic testing/permission recipes merely to replace deleted prose.

## Preserve behavior, not duplication

Before removal, compare the installed skill with a baseline and, where applicable, the implementation or scheduled job it describes. A newer date alone does not establish which conflicting workflow is correct. Keep a recoverable backup outside active skill discovery; omit generated runtimes from source backups.

Classify findings as new regressions, inherited defects, or intentional policy changes. Separate preserving an asset from proving it works. When merging, retain unique assets; delete exact duplicates only after updating their callers. Resolve script dependencies relative to the script rather than former skill locations.

Keep narrow decision boundaries: distinguish an authorized operation from a diagnostic check, persistent user state from task-owned resources, and optional metadata gaps from actual failures.

## Checks that matter

- Use Hermes' active discovery to distinguish installed skills from `.archive`, platform-disabled entries and hidden backup content. Validate frontmatter and duplicate names within active roots, not a raw recursive total. Account for symlinked skills when comparing backups: a copied backup may contain their files while `Path.rglob` skips the live directory symlink, creating false deletion reports.
- Check root-relative links and executable callers as well as tool names, related-skill metadata, Telegram bindings and scheduled prompts. A skill rename can leave injected memory references stale too.
- For code-bearing skills, exercise affected behavior with isolated fixtures and syntax checks. A fixture passing is not a live service test; label that boundary.
- Recheck exact targets after edits. Whole-body rewrites must leave one intended body: a frontmatter-only search/replace has previously appended a second body instead of replacing it. Use an explicit complete rewrite or unique full section, then verify headings and routing.
- Compare the final tree with the backup to catch unplanned deletion or generated runtime changes. Keep configuration and external side effects out of a documentation cleanup unless needed and authorized.

## Portability preparation

Reuse existing variable names from the private environment file and its public example; avoid parallel aliases for the same setting. Move duplicated shell exports only after comparing effective values without printing them, and preserve the private file's `0600` mode. Distinguish a script that reads a variable from agent guidance and separately configured external dependencies. Verify precedence, missing-setting failures and paths with spaces using isolated fixtures; neither environment exports nor a documentation rewrite prove an external browser or scheduler has adopted them. Keep local values, backups and runtime state outside a prospective public export.

Compare external helper implementations read-only before claiming portability. A context manager may restart a service on entry even after a separate readiness check; do not label such a sequence side-effect-free. Document unsupported settings and require a separately scoped compatibility change instead of silently editing the external project.

Classify source-scan hits against their baseline: generic upstream examples and pre-existing public Git identity are not newly introduced machine dependencies or credentials. Keep these exclusions explicit; a targeted portability scan is not a complete secret or history audit.

Report the concrete changes, executed checks and remaining limits. Do not shorten every skill or delete useful safeguards just to hit a global size target.
