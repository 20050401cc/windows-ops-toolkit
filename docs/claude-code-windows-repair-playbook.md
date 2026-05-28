# Claude and Local Agent Windows Repair Playbook

This is a generic troubleshooting checklist for local agent tools on Windows.
It intentionally avoids real API keys, private endpoints, and machine-specific
paths.

## First Checks

1. Confirm which product is failing: desktop app, CLI, local web UI, or bridge.
2. Check whether the process is still running.
3. Check whether the expected port is listening.
4. Read the latest log instead of repeatedly relaunching.
5. Verify the model/provider name is accepted by the target tool.

## Common Failure Areas

- stale background process
- wrong working directory
- missing runtime such as Node, Python, Bun, or Git
- expired login
- API key placed in the wrong variable
- local security software deleting helper scripts
- bridge server returns HTTP 200 but streaming/tool calls still fail

## Recovery Pattern

1. Stop duplicate processes.
2. Start the smallest official path first.
3. Verify one direct command works.
4. Add bridge or launcher layers only after the direct path works.
5. Keep provider-specific launchers separate from each other.
6. Never write real keys into docs, Git history, or shared config.
