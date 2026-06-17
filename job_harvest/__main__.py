from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect, enrich, and review job postings.")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to YAML config file. Default: config.yaml",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Install Python dependencies from requirements.txt.")
    setup_parser.set_defaults(command="setup")

    init_parser = subparsers.add_parser("init-config", help="Create config.yaml from config.example.yaml if missing.")
    init_parser.set_defaults(command="init-config")

    run_parser = subparsers.add_parser("run", help="Run the collector once from YAML config.")
    run_parser.set_defaults(command="run")

    schedule_parser = subparsers.add_parser("schedule", help="Run the collector on a schedule from YAML config.")
    schedule_parser.set_defaults(command="schedule")

    query_parser = subparsers.add_parser("show-queries", help="Print generated queries from YAML config.")
    query_parser.set_defaults(command="show-queries")

    serve_parser = subparsers.add_parser("serve", help="Start the web server.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--reload", action="store_true")

    test_parser = subparsers.add_parser("test", help="Run the unittest suite.")
    test_parser.set_defaults(command="test")

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parents[1]

    if args.command == "setup":
        requirements_path = root_dir / "requirements.txt"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
        return

    if args.command == "init-config":
        source = root_dir / "config.example.yaml"
        target = Path(args.config).expanduser()
        if target.exists():
            print(f"[job_researcher] config already exists: {target}")
            return
        shutil.copyfile(source, target)
        print(f"[job_researcher] created {target} from {source.name}")
        return

    if args.command == "run":
        from job_harvest.config import load_config
        from job_harvest.runner import run_collection

        config = load_config(args.config)
        postings, run_dir = run_collection(config)
        print(f"[job_researcher] saved {len(postings)} postings to {run_dir}")
        return

    if args.command == "schedule":
        from job_harvest.scheduler import run_scheduler

        run_scheduler(args.config)
        return

    if args.command == "show-queries":
        from job_harvest.config import build_queries, load_config

        config = load_config(args.config)
        for query in build_queries(config.criteria, config.search.queries):
            print(query)
        return

    if args.command == "test":
        subprocess.check_call(
            [sys.executable, "-m", "unittest", "discover", "-s", str(root_dir / "tests"), "-v"]
        )
        return

    import uvicorn
    from job_harvest.server import create_app

    if args.reload:
        uvicorn.run(
            "job_harvest.server:create_app",
            host=args.host,
            port=args.port,
            reload=True,
            factory=True,
        )
        return

    uvicorn.run(create_app(), host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
