#!/usr/bin/env node

import { accessSync, constants } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const rootDir = dirname(dirname(fileURLToPath(import.meta.url)));
const args = process.argv.slice(2);

function isExecutable(path) {
  try {
    accessSync(path, constants.X_OK);
    return true;
  } catch (_error) {
    return false;
  }
}

function candidatePythons() {
  const candidates = [];
  if (process.env.JOB_RESEARCHER_PYTHON) {
    candidates.push(process.env.JOB_RESEARCHER_PYTHON);
  }
  candidates.push(join(rootDir, ".venv", "bin", "python"));
  candidates.push(join(rootDir, ".venv", "Scripts", "python.exe"));
  candidates.push("python3");
  candidates.push("python");
  candidates.push("py");
  return candidates;
}

function runWithPython(command) {
  const pythonArgs = command === "py" ? ["-3", "-m", "job_researcher", ...args] : ["-m", "job_researcher", ...args];
  return spawnSync(command, pythonArgs, {
    cwd: rootDir,
    stdio: "inherit",
    shell: false,
  });
}

for (const command of candidatePythons()) {
  if (command.includes("/") || command.includes("\\")) {
    if (!isExecutable(command)) {
      continue;
    }
  }
  const result = runWithPython(command);
  if (result.error && result.error.code === "ENOENT") {
    continue;
  }
  process.exit(result.status ?? 1);
}

console.error("Python was not found. Install Python 3.11+ or set JOB_RESEARCHER_PYTHON.");
process.exit(1);

