import json, pathlib, datetime
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
state = {
    "state": "idle",
    "commit": None,
    "run_script": None,
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
print("State -> idle")
