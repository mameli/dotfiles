# YouTube prompt/system-prompt extraction

When a user shares a YouTube link and asks for “the prompts”, “system prompts”, “instructions”, or similar, do not stop at a normal summary. Treat prompt recovery as an evidence task:

1. Fetch the transcript first and summarize the video normally.
2. Extract any prompts or instruction snippets explicitly mentioned in the transcript, preserving wording and labeling them as transcript-derived.
3. If the video is about a public tool/package and the transcript references a specific plugin, skill, command, or benchmark, look for authoritative upstream artifacts (npm package metadata/tarball, GitHub repository files, package README, bundled skill/command files) to recover the actual prompt text.
4. Label the provenance for each prompt block clearly:
   - `mentioned in the video/transcript`
   - `reconstructed from transcript description`
   - `from upstream package/source file`
5. Do not claim a reconstructed prompt is the exact system prompt unless it came from an authoritative source file or direct quote.
6. Prefer concise blocks of reusable prompt text over dumping unrelated repository files.

Useful pattern for npm-distributed AI-agent plugins:

```bash
npm view <package-name> --json
TMP=$(mktemp -d)
cd "$TMP" && npm pack <package-name>@<version> >/dev/null
 tar -xzf <package-name>-<version>.tgz
find package -maxdepth 3 -type f | sort
```

Then inspect likely files such as:

- `skills/*/SKILL.md`
- `.opencode/command/*.md`
- `hooks/*instructions*`
- `README.md`

For user-facing output, include: short video summary, prompts/instructions found, and a practical takeaway.