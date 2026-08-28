# Agent Skills

Source of truth for the maintainer's agent skills. Each skill is a directory
under `skills/` holding a `SKILL.md` with `name` and `description` frontmatter.
Nothing here names a particular agent: any agent that loads skills in this
format can read them.

Always-on policy text belongs in `agent-rules`, not here. A skill is loaded on
demand, so it carries the longer procedure a rule only points at.

## Skills

- **`human-handoff`** — Decide whether to ask a person at all, then shrink
  whatever is left to something they can paste in one shot.

## Installing

Skills are not copied into an agent home. They are linked, so the checkout is
the only copy and drift is impossible.

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
