# Local repository inspection

For repository size or language composition requests, use `pygount --format=summary .` or `--format=json`, excluding generated/dependency directories such as `.git,node_modules,venv,.venv,dist,build`. Distinguish generated, duplicate, binary, unknown and empty categories from handwritten code.

Before committing requested changes, inspect the intended diff and run checks appropriate to the affected behavior. Do not turn a read-only GitHub request into an implementation or pre-commit audit.

Use the canonical assets listed in `SKILL.md`: `scripts/gh-env.sh`, issue/PR `templates/`, and the command, CI, commit and review references. For implementation, testing, or pre-commit review procedures, load `software-delivery-workflows`; do not require it for read-only inspection.
