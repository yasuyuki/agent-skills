# Agent Skills

The maintainer's agent skills, published from the canonical `agent-rules` source. Each
skill is a directory under `skills/` holding a `SKILL.md` with `name` and
`description` frontmatter. Nothing here names a particular agent: any agent that
loads skills in this format can read them.

Skills are placed the same way always-on rules are — copied from the canonical
source into each agent's skills directory and compared byte for byte — so the
copies here are published output, not the working copy. Edits belong upstream.

Always-on policy text belongs in `agent-rules`, not here. A skill is loaded on
demand, so it carries the longer procedure a rule only points at.

## Skills

- **`human-handoff`** — Decide whether to ask a person at all, then shrink
  whatever is left to something they can paste in one shot.
- **`maintain-environment-inventory`** — Keep environment references and every
  agent's management skill placement consistent when changing or selecting a runtime.

## Installing

Link a skill into your agent's skills directory, so the checkout stays the only
copy and `git pull` is the whole update.

`<checkout>` is wherever this repository is cloned, `<skills-dir>` is the
directory your agent reads skills from, and `<name>` is one of the skills above.

Windows (no administrator rights needed):

```console
cmd /c mklink /J "<skills-dir>\<name>" "<checkout>\skills\<name>"
```

WSL, where `<checkout>` is the same directory reached through `/mnt/<drive>`:

```console
ln -s <checkout>/skills/<name> <skills-dir>/<name>
```

A distro with Windows drive automount disabled cannot reach this checkout and
is out of scope for linking.

## License

MIT. See `LICENSE`.
