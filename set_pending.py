import json, pathlib, datetime, subprocess, sys
commit = subprocess.check_output(["git", "rev-parse", "--short=7", "HEAD"]).decode().strip()
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
state = {
    "state": "pending",
    "commit": commit,
    "run_script": "remote_gpu_run.sh",
    "pid": None,
    "started_at": None,
    "finished_at": None,
    "exit_code": None,
    "error": None,
    "updated_at": now,
}
tmp = pathlib.Path(".gpu_state.json.tmp")
tmp.write_text(json.dumps(state, indent=2) + "\n")
tmp.replace(".gpu_state.json")
print("State -> pending (commit=" + commit + ")")
