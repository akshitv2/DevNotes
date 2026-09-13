# Claude Code — Detailed Notes

---

## 1. What Claude Code Is

Agentic coding tool that reads your codebase, edits files, runs shell commands, and integrates with dev tools (git,
GitHub/GitLab, MCP servers, browsers). Provides following interfaces:

- **Terminal CLI** — the full-featured original, `claude` command
- **VS Code extension/JetBrains plugin/Cursor**
- **Desktop app** (macOS, Windows, Linux beta) — visual diffs, parallel sessions, scheduling
- **Web** — claude.ai/code, run tasks with no local setup, works from mobile too
- **Slack** (`@Claude` mentions), **GitHub Actions**, **GitLab CI/CD**, **Chrome extension** (browser automation)

### Core capabilities

- Explore/understand codebases, trace execution paths
- Fix bugs from an error message or symptom description
- Build features across multiple files
- Git workflows: commit, branch, **create PRs** (`gh pr create`) directly
- Connect external tools via **MCP** (Jira, Slack, databases, Google Drive, etc.)
- Customize via **CLAUDE.md**, **auto memory**, **skills**, **hooks**
- Run **subagents** in parallel; **agent teams**; the **Agent SDK** for fully custom agents
- **Schedule** recurring work: Routines (cloud), Desktop scheduled tasks, `/loop`

---

General diagnostic tool: **`claude doctor`** — checks PATH, binary integrity, keychain, shell config, and more in one
shot.

---

## 2. CLAUDE.md and Memory (the most important customization mechanism)

Every session starts with a **fresh context window**. Two mechanisms carry knowledge across sessions:

### CLAUDE.md (you write it)

Markdown file with persistent instructions, loaded at the start of every session as a **user message** (not baked into
the system prompt — so it's followed, not enforced).

**Locations, in load order (broad → specific; later = read last = weighted more):**

| Scope                                               | Location                                    | Shared with                           |
|-----------------------------------------------------|---------------------------------------------|---------------------------------------|
| Managed/org policy Linux/WSL/C: (Program files Win) | Everyone on the machine, cannot be excluded |                                       |
| User                                                | `~/.claude/CLAUDE.md`                       | Just you, all projects                |
| Project                                             | `./CLAUDE.md` or `./.claude/CLAUDE.md`      | Team, via git                         |
| Local                                               | `./CLAUDE.local.md`                         | Just you, this project — gitignore it |

Run **`/init`** to auto-generate a starting CLAUDE.md by having Claude analyze the codebase (build commands,
conventions, structure). It won't clobber an existing file — it proposes edits instead.

**Writing effective CLAUDE.md:**

- Keep it **under ~200 lines**; larger files burn context and reduce how reliably instructions are followed
- Use headers/bullets, not dense prose
- Be concrete and *verifiable*: "Use 2-space indentation" beats "format code properly"
- Watch for contradictions across nested CLAUDE.md files — Claude may pick one arbitrarily
- `@path/to/file` import syntax pulls in other files (max depth 4); wrap in backticks to mention a path *without*
  importing it
- If you already have `AGENTS.md` (shared with other coding agents), just add `@AGENTS.md` at the top of `CLAUDE.md`, or
  symlink `CLAUDE.md → AGENTS.md`
- **`.claude/rules/*.md`** — split large CLAUDE.md into topic files; add YAML frontmatter `paths: ["src/api/**/*.ts"]`to
  make a rule load *only* when Claude touches matching files (saves context)
- In big monorepos, use `claudeMdExcludes` to skip irrelevant ancestor CLAUDE.md files

### Auto memory (Claude writes it, on its own)

Claude automatically saves 4 kinds of notes to `~/.claude/projects/<project>/memory/`:

- `user` — your role/preferences
- `feedback` — corrections you've given
- `project` — ongoing work/decisions not derivable from code
- `reference` — where to find external info (ticket tracker, dashboard, etc.)

It skips anything derivable from the codebase or already in CLAUDE.md. Only the first 200 lines / 25KB of the`MEMORY.md`
index load at session start; topic files load on demand. On by default; toggle with `/memory` or
`autoMemoryEnabled: false` in settings.

### Real Problem: "Claude isn't following my CLAUDE.md"

1. Run `/context` → check **Memory files** actually loaded the file you edited
2. Verify the file is in a location that's actually loaded for *this* session (see table above)
3. Make instructions more specific/concrete
4. Check for **conflicting instructions** across files
5. If it's something that must happen *every time* deterministically (before every commit, after every edit) — **that's
   not a CLAUDE.md job, it's a hook job.** CLAUDE.md is guidance; hooks are enforcement.

### Real Problem: "My CLAUDE.md is too large / instructions vanish after `/compact`"

- Root CLAUDE.md **does** survive `/compact` (Claude re-reads it from disk). Nested/path-scoped rules only reload when
  Claude touches matching files again.
- If an instruction disappeared, it was likely stated only in chat, not written to CLAUDE.md — conversation-only
  instructions don't survive compaction.
- Run `/doctor` — it proposes trims for a checked-in CLAUDE.md (cuts derivable content, keeps non-obvious
  pitfalls/conventions).

---

## 5. Everyday Workflows (prompt recipes)

- **Codebase overview**: "give me an overview of this codebase" → then narrow: "explain the main architecture
  patterns", "what are the key data models?"
- **Find code**: "find the files that handle user authentication" → "trace the login process from front-end to database"
- **Fix a bug**: paste the error / reproduction command → "suggest a few ways to fix X" → "update file.ts to add the
  fix"
- **Refactor**: "find deprecated API usage" → get suggestions → apply in **small, testable increments** → run tests
- **Tests**: "find functions in X not covered by tests" → "add tests" → "add edge case tests" → "run the new tests and
  fix failures"
- **PRs**: just say "create a pr" — Claude stages, writes the message, and runs `gh pr create` / `glab mr create`. Find
  that session later with `claude --from-pr 1234`.
- **Docs**: "find functions without JSDoc in the auth module" → generate → review
- **Images**: drag-drop, `Ctrl+V` paste, or give a path. Great for screenshots of errors, UI mockups → CSS, diagrams →
  schema changes
- **@-references**: `@src/utils/auth.js` includes a file's full content instantly; `@src/components` lists a directory;
  `@github:repos/owner/repo/issues` pulls MCP resource data
- **Resume work**: `claude --continue` (most recent session in this dir), `claude --resume` (picker), or `/resume`inside
  a session
- **Parallel work**: `claude --worktree feature-auth` in one terminal, a different worktree name in another — isolated
  checkouts, no edit collisions. Monitor many from one screen with **agent view** (`claude agents` / background
  sessions).
- **Plan before editing**: `claude --permission-mode plan` or `Shift+Tab` to plan mode — Claude researches and proposes
  without touching files until you approve
- **Delegate research to a subagent**: "use a subagent to investigate how our auth system handles token refresh" — keeps
  your main context clean since only the summary comes back
- **Pipe into scripts**: `git log --oneline -20 | claude -p "summarize these commits"` — full Unix philosophy support,
  use in CI/pre-commit hooks

### Scheduling recurring tasks — pick the right one

| Option                      | Runs where                          | Best for                                                                                                          |
|-----------------------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Routines**                | Cloud (even when your laptop's off) | PR reviews, dependency audits, anything that should run unattended; can trigger on API calls or GitHub events too |
| **Desktop scheduled tasks** | Your machine via Desktop app        | Needs local files/tools/uncommitted changes                                                                       |
| **GitHub Actions**          | Your CI                             | Repo-event-tied or cron-in-workflow-config tasks                                                                  |
| **`/loop`**                 | Current CLI session only            | Quick polling; dies when the session ends                                                                         |

---

*End of Part 1. Say "next" and I'll continue with: Permission modes & Auto mode, Hooks, MCP, Subagents, Skills &
Plugins, Settings, Sandboxing/Security, and a bigger troubleshooting reference for runtime errors, context/cost
management, and CI/CD integration.*

---

# Part 2: Permissions, Hooks, MCP, Subagents

## 6. Permission Modes

Every action Claude takes either runs automatically or prompts you first — the **permission mode** decides where that
line is.

| Mode                   | Config value        | What runs without asking                                                                                      | Best for                                                                                      |
|------------------------|---------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **Manual**             | `default`           | Reads only                                                                                                    | Reviewing every action, sensitive work                                                        |
| **Accept Edits**       | `acceptEdits`       | Reads + file edits + safe filesystem commands (`mkdir`, `touch`, `mv`, `cp`, `rm`, `sed`) in your working dir | Iterating on code you'll review via `git diff` after                                          |
| **Plan**               | `plan`              | Reads, plus classifier-approved commands during research                                                      | Explore before touching anything                                                              |
| **Auto**               | `auto`              | Everything, reviewed in the background by a separate classifier model                                         | Long tasks, less prompt fatigue — **this is the default starting mode on Pro/Max/Team plans** |
| **Don't Ask**          | `dontAsk`           | Reads + pre-approved tools; anything else is **denied**, never asked                                          | Locked-down CI/scripts                                                                        |
| **Bypass Permissions** | `bypassPermissions` | Everything, no checks                                                                                         | **Only** in isolated containers/VMs — never on your host machine                              |

Cycle modes with **`Shift+Tab`**. Start a session in a specific mode: `claude --permission-mode plan`.

### Auto mode (the default you'll hit first)

A separate **classifier model** (Sonnet 5 by default) reviews each risky action instead of you. It blocks things like:

- `curl | bash`, sending secrets externally, production deploys/migrations, force pushes, mass cloud-storage deletion,
  `git reset --hard`/`rm -rf` on uncommitted work, merging your own unreviewed PR, disabling CI checks, printing live
  credentials, tunneling a local service to the public internet.

It allows by default: local file ops in your working dir, installing deps from lockfiles, reading `.env` and sending its
creds to the matching API, read-only HTTP, pushing to any branch of the current repo (including default branch), opening
a PR that matches your request.

**Real problem: "auto mode keeps blocking something routine (like pushing to our internal registry)."**
→ The classifier only trusts your working directory and its originally-configured git remotes. Anything else (internal
buckets, internal package registries, deploy targets) is unknown to it by default. Fix: an admin adds it to
`autoMode.environment` as **trusted infrastructure** (see `/docs/en/auto-mode-config`), or you say "don't push" / stated
boundaries in chat (session-only, lost on compaction — use a `deny` rule for a hard guarantee).

**Real problem: "Claude keeps getting auto-denied and stuck."**
→ After 3 consecutive or 20 total blocks in a session, auto mode **pauses** and falls back to prompting you. Approve the
action once to resume auto mode. Use `/feedback` to report false positives.

**Real problem: "I want auto mode to double-check before deploys/prod DB changes even though it's usually fine."**
→ Add `permissions.ask` rules for those specific commands — ask rules always force a real prompt, even in auto mode.

### Protected & critical paths (apply in **every** mode except bypass)

- **Protected paths** (`.git`, `.claude`, `.vscode`, `.npmrc`, shell rc files, etc.) always prompt for writes — even an
  explicit `allow` rule in settings can't silently approve them.
- **Critical paths** (filesystem root, home dir, your working directory's parents, drive roots) can never be `rm -rf`'d
  via an allow rule or hook `"allow"` — this is a hard circuit breaker against model error, distinct from normal
  permission rules.

---

## 7. Hooks — deterministic automation

Hooks are shell commands (or HTTP/MCP/LLM calls) Claude Code runs automatically at fixed lifecycle points — **use these
when you need something to *always* happen**, not just usually happen (that's what CLAUDE.md is for).

### Key events

| Event                            | Fires                                                                                |
|----------------------------------|--------------------------------------------------------------------------------------|
| `SessionStart`                   | Session begins/resumes (matcher: `startup`,`resume`,`clear`,`compact`,`fork`)        |
| `UserPromptSubmit`               | Before your prompt reaches Claude                                                    |
| `PreToolUse`                     | Before a tool call — **can block it**                                                |
| `PermissionRequest`              | Right when Claude Code is about to show you a permission prompt — can auto-answer it |
| `PostToolUse`                    | After a tool call succeeds                                                           |
| `Stop`                           | When Claude finishes responding (not on interrupts)                                  |
| `SubagentStart` / `SubagentStop` | Subagent lifecycle                                                                   |
| `PreCompact` / `PostCompact`     | Around context compaction                                                            |
| `Notification`                   | Claude needs input/permission — great for desktop alerts                             |

### How a hook communicates

Reads JSON on **stdin**, replies via **exit code** + stdout/stderr:

- **Exit 0**: no objection (normal flow continues); for some events, stdout is injected as context
- **Exit 2**: **block** the action; stderr becomes Claude's feedback
- **Structured JSON on stdout** (exit 0): fine-grained control, e.g.
  `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}`

### The 4 hooks everyone sets up first

1. **Notification hook** — desktop alert when Claude needs input (`osascript`/`notify-send`/PowerShell MessageBox)
2. **Auto-format after edits** — `PostToolUse` on `Edit|Write` →
   `jq -r '.tool_input.file_path' | xargs npx prettier --write`
3. **Block edits to protected files** — `PreToolUse` on `Edit|Write`, script checks path against `.env`/
   `package-lock.json`/`.git/`, exits 2 to block
4. **Re-inject context after compaction** — `SessionStart` with `matcher: "compact"` → echoes reminders back into
   context

### Real Problem: "My hook's JSON output has no effect"

Two usual causes:

- **Something else writes to stdout first** — most commonly an unconditional `echo` in your shell profile (`.bashrc`/
  `.zshrc`) that gets prepended, so the combined output no longer starts with `{` and Claude Code can't parse it as
  JSON. Fix: wrap profile echoes in `if [[ $- == *i* ]]; then ... fi` (only run in interactive shells).
- **A field at the wrong nesting level** — e.g. `permissionDecision` must be inside `hookSpecificOutput`, not top-level.
  Misplaced fields are silently ignored (check with `claude --debug`, search for "Hook JSON output had unrecognized
  keys").

### Real Problem: "Hook error in output" / "command not found"

- Script exited non-zero unexpectedly → test manually: `echo '{"tool_name":"Bash",...}' | ./my-hook.sh; echo $?`
- "command not found" → use `"$CLAUDE_PROJECT_DIR"/.claude/hooks/script.sh` (absolute path), not a relative one
- Script not executable → `chmod +x`
- "jq: command not found" → install jq or rewrite in Python/Node

### Real Problem: "Stop hook loop / Claude won't stop"

Claude Code force-stops a `Stop` hook after **8 consecutive blocks with no progress**. If your hook needs more
iterations, check the `stop_hook_active` field on the JSON input and exit 0 early to avoid infinite blocking, or raise
`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`.

### Real Problem: "Hooks aren't firing at all"

- Check `/hooks` — confirms registration and matcher
- Matchers are **case-sensitive** and exact (`Edit|Write`, not `edit|write`)
- Verify you used the right event (`PreToolUse` fires *before*, `PostToolUse` *after*)
- Settings file edits are usually picked up live, but if not, restart the session

### Security note

Only **exit-2 deny decisions in `PreToolUse`** are unconditionally enforced — they apply even in `bypassPermissions`
mode, which is the mechanism for org-wide guardrails users can't bypass by switching modes. The reverse isn't true: a
hook returning "allow" can't override a real `deny` rule from settings.

---

## 8. MCP (Model Context Protocol) — connecting external tools

MCP servers give Claude tools beyond its built-ins: query a database, search Jira, drive a browser, hit
Sentry/Linear/Notion, etc.

### Quickest path

```bash
# Hosted (HTTP) server, no auth
claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp

# Local (stdio) server — runs as a subprocess via npx
claude mcp add playwright -- npx -y @playwright/mcp@latest

# Check status
claude mcp list
```

Status glyphs: `✔ Connected` / `! Needs authentication` / `✘ Failed to connect` / `⏸ Pending approval` /
`⊘ Disabled for this project`.

### Scopes (where the config lives)

| Scope             | File                                         | Available to                            |
|-------------------|----------------------------------------------|-----------------------------------------|
| `local` (default) | `~/.claude.json`, under this project's entry | Just you, this project                  |
| `project`         | `.mcp.json` in project root                  | Anyone who clones the repo (commit it!) |
| `user`            | `~/.claude.json`, top-level `mcpServers`     | Just you, every project                 |

`claude mcp add --scope project ...` → commit `.mcp.json` → teammates get a one-time approval prompt and then it just
works.

### Manual config example (`.mcp.json`)

```json
{
  "mcpServers": {
    "claude-code-docs": {
      "type": "http",
      "url": "https://code.claude.com/docs/mcp"
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ]
    }
  }
}
```

### OAuth-gated servers (Sentry, Linear, Notion, GitHub…)

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# then inside a session:
/mcp   # select sentry → Authenticate → completes in browser
```

Static-token servers instead: `--header "Authorization: Bearer <token>"` at add time.

### Real Problem: "/mcp shows No MCP servers configured"

- You ran `claude mcp add` from a **different project** — local-scope servers are tied to the directory (repo root)where
  you added them. Re-add from the right project, or use `--scope user`.
- You edited the wrong file — only `~/.claude.json` and `<project>/.mcp.json` are read. Not `~/.claude/mcp.json` or
  similar.
- Malformed JSON entry — Claude Code silently skips it; `claude mcp list` shows the parse warning.

### Real Problem: "Failed to connect" / "Connection error"

1. Check `claude mcp get <name>` for the exact HTTP status/error text
2. For HTTP servers: `curl -I <url>` — a `404`/`405` still confirms reachability (many MCP endpoints only answer POST);
   `401`/`403` means you need to authenticate; no response = network/URL problem
3. For stdio servers: run the exact command yourself in a terminal (e.g. `npx -y @playwright/mcp@latest`) to see the
   real underlying error — usually missing Node.js, a missing browser, or a missing `--` separator in how you registered
   it

### Real Problem: "Connection timed out at startup"

First run of an `npx`-based server can be slow while it downloads. Raise the default 30s timeout:
`MCP_TIMEOUT=60000 claude`.

### Real Problem: "Server connects but shows zero tools"

Usually a missing required env var (API key). Pass it via `--env KEY=value` on `claude mcp add`, or the `env` field in
`.mcp.json`. Check the server's own docs for what it needs.

### Real Problem: "I edited .mcp.json but nothing changed"

`.mcp.json` is read only at **session start** — restart the session. If servers still don't show, check`claude mcp list`
for parse warnings. If you previously declined the approval prompt, reset it:`claude mcp reset-project-choices`.

### Cost note

Each connected server's tool names and instructions load into **every session's context window**. Remove servers you're
not using.

---

## 9. Subagents — isolated context workers

A subagent runs in its **own fresh context window** with its own system prompt, tool access, and model. Use one when a
side task (log analysis, big codebase search, verbose test output) would flood your main context with things you don't
need to keep around — only the subagent's final summary comes back.

### Built-in subagents (auto-used)

- **Explore** — fast, read-only codebase search (inherits your model, capped at Opus)
- **Plan** — research agent used during plan mode
- **general-purpose** — full toolset, for complex multi-step delegated work

### Creating your own

Just ask Claude: *"Create a personal code-improver subagent in ~/.claude/agents/ that scans files for
readability/performance issues, read-only, using Sonnet."* Claude writes a markdown file with YAML frontmatter:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
---

You are a code reviewer. For each issue, explain the problem, show the current
code, and provide an improved version.
```

- **`.claude/agents/`** = project scope (commit it, team-shared)
- **`~/.claude/agents/`** = personal, all your projects
- The **`description`** field is what drives *automatic* delegation — write it as a trigger condition ("reviews code for
  security issues before commits"), not just a capability label. Vague descriptions route poorly.

### Real Problem: "Claude never delegates to my custom subagent"

Almost always a weak `description`. Compare "security expert" (rarely triggers) vs. "Proactively reviews code for
security vulnerabilities immediately after code changes" (triggers reliably). You can also force it:
`@code-reviewer look at the auth changes`, or make the whole session run as that agent: `claude --agent code-reviewer`.

### Real Problem: "Too many custom subagents and delegation got worse"

Combined subagent descriptions have a **15,000-token budget**; past that Claude Code warns at startup. More importantly,
flooding Claude with overlapping options makes automatic routing less reliable — most teams settle on a handful of
well-scoped agents, not a sprawling roster.

### Real Problem: "Subagent work isn't being remembered between sessions"

Add `memory: project` (or `user`/`local`) to the frontmatter — gives that subagent a persistent notes directory (
separate from main-conversation auto memory) it reads/writes on its own.

### Real Problem: "Subagent can run destructive commands I didn't expect"

Restrict with `tools:` (allowlist) or `disallowedTools:` (denylist) in frontmatter, and/or add a `PreToolUse` hook in
the subagent's own frontmatter to validate commands (e.g. a DB-read-only subagent that greps for
`INSERT|UPDATE|DELETE|DROP` and exits 2 to block).

### Subagents vs. Skills vs. Agent Teams vs. Forks — pick the right tool

| Need                                                                           | Use                                                                                           |
|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Reusable *instructions/knowledge* for the main conversation                    | **Skill**                                                                                     |
| Isolate exploration/verbose output, get back a summary                         | **Subagent**                                                                                  |
| Multiple sessions that must talk to *each other* / coordinate                  | **Agent teams** (heavier, ~7x tokens in plan-heavy work)                                      |
| A side task that needs your *whole* conversation history without re-explaining | **Fork** (`/subtask`) — inherits everything, only its own tool calls stay out of your context |

### Chaining & parallel patterns

```text
Research the authentication, database, and API modules in parallel using separate subagents
```

```text
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

Caution: running many subagents that each return **detailed** results can itself consume significant context — ask for
terse summaries.


---

# Part 3: Skills, Plugins, Settings, Sandboxing, Cost/Context Management

## 10. Skills — reusable instructions & procedures

A **skill** is a `SKILL.md` file (YAML frontmatter + markdown instructions) that Claude loads **on demand**, not into
every session's baseline context — the opposite tradeoff from CLAUDE.md. Custom slash commands (`.claude/commands/*.md`)
have been merged into skills; a command file still works, but a skill folder additionally supports supporting files and
finer invocation control.

**Rule of thumb:** if you keep pasting the same instructions/checklist into chat, or a CLAUDE.md section has grown into
a multi-step *procedure* rather than a fact — that's a skill, not a CLAUDE.md entry.

### Minimal skill

```
mkdir -p ~/.claude/skills/summarize-changes
```

```yaml
# ~/.claude/skills/summarize-changes/SKILL.md
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed or wants a commit message.
---
## Current changes
!`git diff HEAD`

  ## Instructions
Summarize the changes above in 2-3 bullets, then list risks.
```

The `` !`command` `` syntax **runs the shell command first** and inlines its live output — this is "dynamic context
injection."

### Where skills live

| Location             | Scope                                                                |
|----------------------|----------------------------------------------------------------------|
| `~/.claude/skills/`  | Personal, all your projects                                          |
| `.claude/skills/`    | Project (commit it)                                                  |
| Plugin's `skills/`   | Wherever the plugin is enabled, namespaced `/plugin-name:skill-name` |
| Managed settings dir | Org-wide                                                             |

### Controlling who can invoke a skill

| Frontmatter                      | You can run it | Claude can run it | Use for                                                                                                                   |
|----------------------------------|----------------|-------------------|---------------------------------------------------------------------------------------------------------------------------|
| (default)                        | Yes            | Yes               | Most skills                                                                                                               |
| `disable-model-invocation: true` | Yes            | No                | Side-effecting actions: `/deploy`, `/commit`, `/send-slack-message` — you don't want Claude deciding to deploy on its own |
| `user-invocable: false`          | No             | Yes               | Background knowledge Claude should just *know*, not a runnable command                                                    |

### Real Problem: "My skill never triggers automatically"

Almost always the `description` field is too vague. Write it as the literal phrases a user would say ("Use when the user
asks what changed, wants a commit message, or asks to review their diff"), not an abstract capability label. Test by
typing one of those phrases verbatim. Also: skill files are discovered at **session start** — a brand-new skill
directory needs a restart (existing skills in an existing directory hot-reload).

### Real Problem: "Skill triggers on the wrong requests / too often"

Narrow the description; or force manual-only with `disable-model-invocation: true`.

### Real Problem: "Skill descriptions keep getting truncated / my skills feel less reliable as I add more"

The full skill listing (names + descriptions) is loaded into context on every turn, budgeted at ~1% of the model's
context window. Once you have many skills, Claude Code shortens/drops descriptions starting with your **least-used**
skills. Run `/skill-doctor` to see the cost and usage of every skill and turn off ones you don't need (
`skillOverrides: {"name": "off"}`).

### Real Problem: "Skill worked, then silently stopped influencing behavior mid-session"

Content isn't gone — Claude is probably just choosing a different approach. Skill content is not re-read on later turns;
strengthen the description/instructions, or enforce deterministically with a **hook** instead. After heavy `/compact`,
older invoked skills can be fully dropped from a shared re-attachment budget — re-invoke the skill if you notice this.

### Run a skill in an isolated subagent

`context: fork` + `agent: Explore` runs the skill's instructions as a background subagent task — good for research-style
skills where you don't want the exploration clogging your main context.

---

## 11. Plugins

Plugins bundle skills, subagents, hooks, and MCP servers into one shareable install. Add a marketplace, then install:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
```

Plugin components load with a namespace prefix (`/my-plugin:skill-name`, `my-plugin:code-reviewer` subagent) so they
never collide with your own. Manage installed plugins and marketplaces from `/plugin`.

**Real Problem: "Installed a plugin but its skill/agent isn't showing up"** — run `/reload-plugins` (or
`/reload-plugins --force` if it warns your next message would re-read the conversation).

---

## 12. Settings — files, precedence, and the array-merge gotcha

Claude Code reads settings from JSON files at several **scopes**:

| Scope          | File                                              | Committed?           | Affects                                                                    |
|----------------|---------------------------------------------------|----------------------|----------------------------------------------------------------------------|
| Managed        | `managed-settings.json` / MDM / claude.ai console | N/A                  | Everyone in the org — can't be overridden (with a few security exceptions) |
| User           | `~/.claude/settings.json`                         | No                   | You, every project                                                         |
| Shared project | `.claude/settings.json`                           | **Yes**              | Everyone who clones the repo                                               |
| Project local  | `.claude/settings.local.json`                     | No (auto-gitignored) | Just you, this project                                                     |

**Precedence (highest wins): Managed → command line (`--settings`) → project local → shared project → user.**

### The #1 real-world gotcha: list keys **merge**, they don't override

`permissions.allow`, `permissions.deny`, etc. defined in multiple files are **combined**, not replaced by the
higher-precedence file. This is why teams get confused: adding `Bash(ls:*)` to your personal `deny` list in
`~/.claude/settings.json` and also to `allow` in `.claude/settings.local.json` does **not** make the local file win —
deny rules combine with allow rules from every scope, and (per the permission rule combination logic) the most
restrictive answer generally applies across an ask/deny vs allow conflict. **Don't assume "closer/more local file always
wins" for permission rules the way it does for plain scalar settings like `model`.**

### Real Problem: "I set a value and it's being ignored"

Checklist, in order:

1. Run `/status` → check **Setting sources** — did the file even load?
2. Is a **higher-precedence** file/flag/env var setting the same key? (`ANTHROPIC_MODEL` env var beats the `model`
   setting from *any* file, for example.)
3. Is this one of the few keys that simply **can't** be set from project/local scope? (e.g.
   `permissions.defaultMode: "auto"` or `"bypassPermissions"` only take effect from user or managed settings — not
   project files.)
4. Is the settings file itself broken? (Strict JSON — no comments, no trailing commas. A syntax error triggers a "
   Settings Error" dialog at startup; run `claude doctor` for details.)
5. For a **committed team key** that a teammate says isn't applying: some keys never apply from a shared repo file at
   all (see the settings reference "Scope" column), and `permissions.allow` / `additionalDirectories` / most `env`values
   only apply after that teammate **trusts the folder**.

### Real Problem: "I picked 'Yes, and don't ask again' but I still get prompted for that command"

That choice writes an `allow` rule to your **local** file — and an `allow` rule there does not outrank an **ask** rule
from a project or managed file. Ask/deny rules from higher scopes still win.

---

## 13. Sandboxing & Security

### The permission system (baseline)

Claude Code asks before file writes, shell commands (beyond a built-in read-only allowlist like `ls`/`cat`/
`git status`), and network access — see Part 2 for permission modes. Writes are, by default, confined to the directory
you started Claude Code in and its subdirectories; reads can go wider but the *first* out-of-scope read prompts you.

### The Bash Sandbox (OS-level, not just prompts)

On **macOS, Linux, and WSL2** (not native Windows — run inside WSL2 there), Claude Code can run Bash commands inside an
OS-enforced sandbox instead of just asking permission each time:

- **Filesystem isolation**: read access to your whole machine (minus denied paths), write access confined to the working
  directory and subdirectories you configure
- **Network isolation**: only domains you allow are reachable; everything else is blocked at the OS level, even if
  Claude tries
- Both matter together — network isolation alone still lets a compromised agent backdoor local files for later access;
  filesystem isolation alone still lets it exfiltrate secrets over the network.
- Enable with `/sandbox` (interactive) or `sandbox.enabled: true` in settings.
- Sandbox writes are still denied to Claude Code's own config/code files even *inside* the writable directory — this
  stops a sandboxed command from granting itself more permissions by editing settings/hooks.

### Real Problem: "Sandboxed command failed even though I approved it"

If the target path is outside the sandbox boundary, approving the *command* doesn't override the *sandbox* — they're two
separate layers. Claude Code will then offer to disable the sandbox and re-run; declining keeps you protected (this is
usually the right call unless you specifically intended the out-of-scope write).

### Protected & critical paths (recap from Part 2)

Even in `acceptEdits`/`auto` mode, writes to `.git`, `.claude`, shell rc files, etc. always prompt, and `rm -rf` against
the filesystem root/home dir/working-directory-parents is never silently approved by an allow rule or hook — this is a
hard circuit breaker independent of your settings.

### Isolation beyond the Bash sandbox

For untrusted/high-autonomy work, layer on stronger isolation: dev containers, a custom container, or a full VM — see "
Sandbox environments" in the docs. `bypassPermissions` mode should **only** ever be used inside one of these, never on
your bare host.

---

## 14. Managing Context & Cost

Claude Code bills by **API tokens** (unless you're on a flat subscription plan absorbing it). Real numbers from
Anthropic's enterprise deployment data: **~$13/developer/active-day, ~$150–250/developer/month** average, with 90% of
users under $30/active-day. The two most common cost blowouts: **long sessions never cleared**, and **leaving Opus as
the default model** for routine work.

### Where the tokens actually go

- **CLAUDE.md** loads in full, every session, every turn — a 5,000-token CLAUDE.md costs 5,000 tokens on message 1 *and*
  message 200. This is the single highest-leverage thing to trim (target <200 lines).
- The **conversation itself** re-sends on every turn (mitigated ~90% by prompt caching, but caching only discounts
  repeated tokens — it doesn't shrink what's being processed).
- **MCP servers** — every connected server's tool descriptions load into context whether you use them that session or
  not.
- **Skill listing** — names+descriptions of all your skills load every turn (see Part 3 §10).
- **Subagents** each get their own separate context window and separate cost.

### Concrete levers, roughly in order of impact

1. **`/clear` between unrelated tasks** — wipes accumulated context back to just CLAUDE.md. Do this every time you
   switch to something genuinely unrelated; don't carry a finished task's context into a new one.
2. **`/compact`** instead of `/clear` when the *old* context is still relevant to the next task — summarizes instead of
   wiping.
3. **Match the model to the task** — Sonnet handles the large majority of routine coding at a fraction of Opus's cost;
   reserve Opus for genuinely hard multi-file/architecture/security work.
4. **Keep CLAUDE.md lean and stable** — trim to what Claude can't infer from the codebase itself, and avoid editing it
   mid-session (invalidates the prompt cache, which is otherwise a ~90% discount on repeated tokens).
5. **Delegate high-volume/verbose work to subagents** — test runs, log analysis, big greps — so only the summary
   re-enters your main (billed-on-every-turn) context.
6. **Disconnect unused MCP servers.**
7. **Turn off unused skills** (`/skill-doctor`, `skillOverrides`).
8. **Check where it's going**: `/usage` for cost/attribution (on paid plans, breaks spend down by
   skill/subagent/plugin/MCP server), `/context` for a live breakdown of what's occupying the context window right now.

### Real Problem: "Usage climbed a lot partway through a long session, seemingly for no reason"

This is usually **context accumulation**, not a harder question — every prior turn gets re-sent as part of the
conversation on each new request. Long sessions also suffer "context rot": older instructions lose weight as more
content piles on top, which is a quality problem as much as a cost one. Fix: clear/compact proactively rather than
letting one session run for hours across unrelated subtasks.


---

# Part 4: Automation, CI/CD, and Consolidated Troubleshooting

## 15. Non-interactive mode (`-p` / `--print`) — the Agent SDK CLI

`-p` turns any `claude` invocation into a one-shot, scriptable batch call: prompt in → result out → exit with a status
code your scripts can branch on.

```bash
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

### Key flags

| Flag                                           | Purpose                                                                                                                                                                                                                 |
|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--bare`                                       | Skip auto-discovery of hooks/skills/subagents/plugins/MCP/auto memory/CLAUDE.md — faster, reproducible across machines. **Recommended for CI.** Needs `ANTHROPIC_API_KEY` since it doesn't use your subscription login. |
| `--output-format json` \| `stream-json`        | Structured output for scripts; `json` includes `total_cost_usd` per invocation                                                                                                                                          |
| `--json-schema '<schema>'`                     | Force output to conform to a JSON Schema, returned in `structured_output`                                                                                                                                               |
| `--allowedTools "Read,Edit,Bash"`              | Pre-approve specific tools so the run never blocks on a prompt                                                                                                                                                          |
| `--permission-mode auto\|acceptEdits\|dontAsk` | Set a baseline instead of listing every tool — **`-p` always starts in Manual mode by default, on every plan**, so you must set this explicitly for CI                                                                  |
| `--permission-prompts none`                    | Deny anything that would need human input rather than hang waiting for it — essential for scheduled/unattended jobs                                                                                                     |
| `--continue` / `--resume <id>`                 | Chain follow-up `-p` calls into the same conversation                                                                                                                                                                   |
| `--append-system-prompt "..."`                 | Add instructions on top of the default system prompt (good for turning Claude into a project-specific linter/reviewer)                                                                                                  |

### Real Problem: "My CI `-p` run hangs forever"

It's waiting on a permission prompt nobody can answer. Add `--permission-prompts none` (denies anything unresolved
instead of hanging) and/or set an explicit `--permission-mode` (`dontAsk` for a hard allowlist, `auto` for
classifier-reviewed autonomy). Piped stdin is also capped at **10MB** — for bigger inputs, write to a file and reference
the path instead of piping.

### Real Problem: "Background dev server / watch process I started got killed"

By design: any background Bash task you start during a `-p` run is terminated ~5 seconds after the final result prints
and stdin closes. `-p` is for single batch invocations, not long-lived services — use an interactive or background
session instead if you need something to keep running after the call returns.

### Useful patterns

```bash
# Pipe data through Claude (build logs, diffs, etc.)
cat build-error.txt | claude -p 'explain the root cause of this build error' > output.txt

# Use as a project-specific linter in package.json
"lint:claude": "git diff main | claude -p \"you are a typo linter...\""

# Structured extraction
claude -p "Extract function names from auth.py" --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}'
```

---

## 16. CI/CD Integration

### GitHub Actions — two ways to set up

1. **Quick setup (recommended)**: inside Claude Code, run `/install-github-app` — walks you through installing the
   GitHub App and secrets, and optionally creates the workflow file for you (as of v2.1.187 you can install just the App
   and skip workflow setup).
2. **Manual**: install the Claude GitHub App → add `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_OAUTH_TOKEN` for Pro/Max
   subscription auth via `claude setup-token`) as a repo secret → copy the example workflow into `.github/workflows/`.

Once set up, mention **`@claude`** in any issue or PR comment and Claude analyzes the code, implements changes, and
pushes commits/opens a PR — respecting your `CLAUDE.md`. You can also trigger it on any GitHub event (opened PR,
schedule, etc.) with a fixed prompt for automated review/triage.

**Real Problem: "@claude isn't responding in comments"** — usually one of: the GitHub App wasn't actually installed on
that repo, the workflow file's trigger condition doesn't match the event (check the `if:` condition matches
`issue_comment` + `contains(...,'@claude')`), or the API key/OAuth token secret is missing/expired.

**Best practices**: define project standards in CLAUDE.md (so CI-run Claude follows the same conventions as your local
sessions), keep credentials in repo secrets (never inline), and set spend/turn limits so a misconfigured trigger doesn't
run wild.

### GitLab CI/CD

Same idea — `@claude` mentions in issues/MRs, quick or manual setup, supports Bedrock/Vertex/Foundry via OIDC.
Configuration lives in `.gitlab-ci.yml` job definitions instead of workflow YAML.

### Agent SDK (build your own automation)

For anything beyond "respond to @claude" — custom orchestration, structured tool-approval callbacks, native message
objects — use the **Agent SDK** (Python/TypeScript packages, or the `-p` CLI as a lighter-weight interface). It gives
you the same agent loop, tools, and context management that power Claude Code itself, callable as a library.

---

## 17. Consolidated Runtime Troubleshooting Reference

### Authentication & authorization

| Error                                                               | Cause / Fix                                                                                                                                                                      |
|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `API Error: 401 Invalid authentication credentials`                 | Token expired — `/login` again; check system clock is accurate (token validation is time-sensitive)                                                                              |
| `This organization has been disabled` (despite active subscription) | A stale `ANTHROPIC_API_KEY` env var is silently overriding your subscription auth. `unset ANTHROPIC_API_KEY`, remove from shell profile, `/status` to confirm active auth method |
| `403 Forbidden`                                                     | Pro/Max: check subscription active at claude.ai/settings. Console: confirm the "Claude Code" or "Developer" role is assigned                                                     |

### Context & requests

| Error                                                    | Cause / Fix                                                                                                                                 |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `Prompt is too long` / `Context exceeds the token limit` | Run `/compact` or `/clear`; check `/context` for what's eating the window (CLAUDE.md, MCP servers, skills, subagent output)                 |
| `Error during compaction: Conversation too long`         | Even the summarization step overflowed — start a fresh session, and next time compact earlier rather than letting a session run to the wall |
| `Model is restricted by your organization's settings`    | Your org's `availableModels` allowlist excludes what you requested — pick from the allowed list or ask an admin                             |

### Server / network

| Error                                        | Cause / Fix                                                                                                                                    |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `API Error: 500` / repeated `529 Overloaded` | Transient — Claude Code auto-retries; if persistent, wait and retry manually                                                                   |
| `Request timed out` / `No response from API` | Check network/proxy; corporate proxies often need `HTTPS_PROXY`/`HTTP_PROXY` set and `NODE_EXTRA_CA_CERTS` pointed at your corporate CA bundle |
| `Unable to connect to Anthropic services`    | Network/firewall blocking the API host — same diagnostic pattern as install-time connectivity issues (Part 1)                                  |

### Usage limits

| Error                                                   | Cause / Fix                                                                                                                                             |
|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `You've hit your session limit` / `spend limit reached` | Check `/usage` for a breakdown by skill/subagent/plugin/MCP server (paid plans) to find the driver; adjust model choice or session hygiene (Part 3 §14) |
| `Credit balance is too low`                             | Add usage credits (subscription) or check Console billing (API)                                                                                         |

### Tool / permission errors

| Error                                    | Cause / Fix                                                                                  |
|------------------------------------------|----------------------------------------------------------------------------------------------|
| `Agent would be spawned with zero tools` | A subagent's `tools:` list has misspelled/unavailable entries — check exact tool names       |
| `subagent_type is required`              | An Agent tool call omitted the type and no `general-purpose` fallback exists in this session |
| `Tool input schema is invalid`           | Usually an MCP server bug — check the server's tool definitions                              |

### General diagnostics

- **`claude doctor`** — one-shot health check: PATH, binary integrity, keychain, shell config, dropped settings entries,
  duplicate subagent names
- **`/status`** — which settings files/managed sources are actually active for this session
- **`/context`** — live breakdown of what's occupying the context window right now
- **`claude --debug`** (or `/debug` mid-session, or `claude --debug-file /tmp/claude.log`) — full hook/tool execution
  log, essential for silently-failing hooks or skills
- **`/doctor`** — proposes CLAUDE.md trims, flags duplicate subagent names, estimates skill-listing context cost

---

## 18. Quick-Reference Cheat Sheet

**Install**: `curl -fsSL https://claude.ai/install.sh | bash` (mac/Linux/WSL) — Windows:
`irm https://claude.ai/install.ps1 | iex`

**Everyday commands**
| Command | Does |
|---|---|
| `claude` | Start interactive session in cwd |
| `claude --continue` / `--resume` | Resume most recent / pick a session |
| `claude --worktree <name>` | Isolated parallel session on its own branch |
| `Shift+Tab` | Cycle permission modes |
| `/init` | Auto-generate CLAUDE.md from the codebase |
| `/memory` | Browse/edit CLAUDE.md, auto memory, toggle auto memory |
| `/context` | See what's filling the context window |
| `/compact` / `/clear` | Summarize / wipe conversation |
| `/agents` (legacy) → now: edit `.claude/agents/*.md` directly, or ask Claude | Manage subagents |
| `/hooks` | Browse configured hooks (read-only view) |
| `/mcp` | Manage/authenticate MCP servers in-session |
| `/skills`, `/skill-doctor` | List skills; find unused/costly ones |
| `/permissions` | View/edit allow-ask-deny rules, recently denied |
| `/usage` | Cost & token breakdown |
| `/status` | Active settings sources, auth method |
| `claude doctor` | Full health check |
| `claude mcp add/list/remove` | Manage MCP servers from the shell |
| `claude -p "..."` | Non-interactive one-shot run |

**Key files**
| File | Purpose |
|---|---|
| `CLAUDE.md` / `.claude/CLAUDE.md` | Project instructions (commit it) |
| `CLAUDE.local.md` | Personal project prefs (gitignored) |
| `~/.claude/CLAUDE.md` | Personal, all projects |
| `.claude/rules/*.md` | Topic-scoped instructions, optionally path-scoped |
| `.claude/settings.json` | Team settings (commit it) |
| `.claude/settings.local.json` | Personal project overrides (auto-gitignored) |
| `~/.claude/settings.json` | Personal global settings |
| `.mcp.json` | Project-scoped MCP servers (commit it) |
| `.claude/agents/*.md` | Subagent definitions |
| `.claude/skills/<name>/SKILL.md` | Skills |
| `~/.claude/agents/`, `~/.claude/skills/` | Personal versions of the above |

---

*End of notes. This covers: install & setup, CLAUDE.md & memory, everyday workflows, permission modes & auto mode,
hooks, MCP, subagents, skills, plugins, settings precedence, sandboxing & security, cost/context management,
non-interactive mode, CI/CD, and a consolidated troubleshooting + cheat sheet. If you want a deeper dive on any single
topic (e.g. Agent SDK internals, agent teams, dynamic workflows, enterprise/managed-settings deployment) — just ask.*
