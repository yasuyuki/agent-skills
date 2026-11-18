# Antigravity tool mapping for pstack

Resolve each tool a pstack skill names to its Antigravity CLI (`agy`)
equivalent here. Delegation, models, permissions and lifecycle still follow
[pstack-runtime](../SKILL.md).

## Tool actions

| pstack action | Antigravity equivalent |
|---------------|------------------------|
| Read a file | `read_file` |
| Create a file | `write_file` |
| Edit a file | `edit_file` |
| Run a shell command | `run_command` (and `manage_task` to inspect, send input to, or kill background tasks) |
| Search file contents / find files | `rg` for contents and `rg --files` or `fd` for files, via `run_command` |
| Fetch a URL / search the web | `search_web`, or `curl` via `run_command` |
| Invoke a skill | `read_file` on the path in the `<skills>` catalog. Read the whole SKILL.md; the native loader may include only the start of a long skill body. |
| Dispatch a subagent | `invoke_subagent` with `TypeName`, `Role`, `Prompt`, `Model` and `Workspace` |
| Dispatch N parallel subagents | N `invoke_subagent` calls in one response |
| Wait for a subagent result | End the turn (call no more tools). Antigravity resumes the session when a subagent sends a message or finishes. |
| Continue or steer a subagent | `send_message` with `Recipient` set to the subagent's `conversationId` and `Message` |
| List or stop subagents | `manage_subagents` with `Action: "list"`, `"kill"` or `"kill_all"` and `ConversationIds` |
| Ask the human a fixed-choice question | `ask_question` with `questions` (`question`, `options`, `is_multi_select`) |
| Schedule a self-paced re-invocation | `schedule` with `DurationSeconds` (one-shot) or `CronExpression` (recurring) and `Prompt` |
| Call an MCP tool | Call it directly as declared in the session's tool list |
| Read this session's transcripts | `~/.gemini/antigravity-cli/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` (or `antigravity` / `antigravity-ide` under `~/.gemini/`). Do not read another product's transcript directory. |

## Subagents

- Use `TypeName: "self"` for a child that writes files, runs commands or uses
  MCP tools. Use `TypeName: "research"` for read-only work that needs no shell
  or MCP access. A read-only child that needs `run_command` or MCP tools gets
  `TypeName: "self"` and a `Prompt` that forbids writing.
- Give each child the absolute path of every SKILL.md it must follow and tell
  it in `Prompt` to read each file in full with `read_file`.
- `invoke_subagent` always runs asynchronously; collect results by ending the
  turn and reading the returned messages.

## Models

`invoke_subagent`'s `Model` accepts `inherit` (the parent's model),
`flash_lite`, `flash` and `pro` (measured on agy 1.5.10,
https://github.com/yasuyuki/work-records/issues/154). Role models come from the
private pstack-settings agy profile. A role set to `inherit-parent` omits
`Model`.

## Source

Adapted from michael-denyer/pstack-claude
`plugins/pstack/skills/poteto-mode/references/agy-tools.md` at
`5ebc35acbf5fc9f9c6537b137e80c61cccf277be`.

MIT License

Copyright (c) 2026 Lauren Tan
Copyright (c) 2026 Michael Denyer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
