# Agent Skills

Source of truth for the maintainer's Claude Code skills. Each skill is a
directory under `skills/` holding a `SKILL.md` with `name` and `description`
frontmatter.

Skills are not copied into an agent home. They are linked, so the checkout is
the only copy and drift is impossible.

`<checkout>` below is wherever this repository is cloned.

Windows (no administrator rights needed):

```console
cmd /c mklink /J "%USERPROFILE%\.claude\skills\<name>" "<checkout>\skills\<name>"
```

WSL, where `<checkout>` is the same directory reached through `/mnt/<drive>`:

```console
ln -s <checkout>/skills/<name> ~/.claude/skills/<name>
```

A distro with Windows drive automount disabled cannot reach this checkout and
is out of scope for linking.

Always-on policy text belongs in `agent-rules`, not here. A skill is loaded on
demand, so it carries the longer procedure a rule only points at.

## License

MIT. See `LICENSE`.
