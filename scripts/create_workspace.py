#!/usr/bin/env python3
"""Create a task workspace with independent Git worktrees (Python 3.9+)."""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / 'template'

def git(*args, cwd=None):
    return subprocess.run(['git', *map(str, args)], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('name', help='Task slug, e.g. fix-auth')
    p.add_argument('--workspace-root', required=True, help='Parent directory for task workspaces')
    p.add_argument('--repo', action='append', required=True, metavar='ALIAS=PATH', help='Repeat for each existing local clone')
    p.add_argument('--base', default='HEAD', help='Git ref used to create each task branch (default: HEAD)')
    p.add_argument('--branch-prefix', default='task/', help='Branch prefix')
    p.add_argument('--yes', action='store_true', help='Proceed without interactive confirmation')
    a = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', a.name): p.error('Invalid task name')
    repos = []
    for spec in a.repo:
        if '=' not in spec: p.error('--repo must be ALIAS=PATH')
        alias, path = spec.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', alias): p.error('Invalid repo alias')
        path = pathlib.Path(path).expanduser().resolve()
        if not path.is_dir(): p.error(f'Not a directory: {path}')
        try:
            git('rev-parse', '--show-toplevel', cwd=path)
            git('rev-parse', '--verify', a.base, cwd=path)
        except subprocess.CalledProcessError: p.error(f'Not a valid Git checkout or base ref: {path}')
        if any(r[0] == alias for r in repos): p.error(f'Duplicate alias: {alias}')
        repos.append((alias, path))
    destination = pathlib.Path(a.workspace_root).expanduser().resolve() / a.name
    if destination.exists(): p.error(f'Destination already exists: {destination}')
    branch = f'{a.branch_prefix}{a.name}'
    for alias, path in repos:
        if subprocess.run(['git', 'check-ref-format', '--branch', branch], cwd=path, capture_output=True).returncode: p.error(f'Invalid branch: {branch}')
        if subprocess.run(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch}'], cwd=path).returncode == 0: p.error(f'Branch already exists in {alias}: {branch}')
    print(f'Workspace: {destination}\nBranch in each repo: {branch}')
    for alias, path in repos: print(f'  {alias}: {path}')
    if not a.yes and input('Create worktrees? [y/N] ').strip().lower() != 'y': return
    destination.mkdir(parents=True)
    created = []
    try:
        for alias, path in repos:
            git('-C', path, 'worktree', 'add', '-b', branch, destination / alias, a.base)
            created.append((alias, path))
        today = datetime.date.today().isoformat()
        descriptions = '\n'.join(f'- `{alias}/` — worktree from `{path}` on `{branch}`' for alias, path in repos)
        for filename in ('AGENTS.md', 'TASK.md', 'WORKLOG.md'):
            content = (TEMPLATE / filename).read_text().replace('{{TASK_NAME}}', a.name).replace('{{DATE}}', today).replace('{{REPOSITORIES}}', descriptions)
            (destination / filename).write_text(content)
        (destination / '.github' / 'skills').mkdir(parents=True)
        print(f'Created {destination}')
    except Exception:
        print('Creation failed. Rolling back created worktrees.', file=sys.stderr)
        for alias, path in reversed(created):
            subprocess.run(['git', '-C', str(path), 'worktree', 'remove', '--force', str(destination / alias)], check=False)
            subprocess.run(['git', '-C', str(path), 'branch', '-D', branch], check=False)
        raise

if __name__ == '__main__': main()
