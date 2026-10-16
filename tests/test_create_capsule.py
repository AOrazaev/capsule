import contextlib
import importlib.util
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'create_capsule.py'
SPEC = importlib.util.spec_from_file_location('create_capsule', SCRIPT)
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class CreateCapsuleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        self.repos = {}
        for alias in ('api', 'frontend'):
            repo = self.root / 'repos' / alias
            repo.mkdir(parents=True)
            workspace.git('init', repo)
            workspace.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                          '-c', 'commit.gpgsign=false', 'commit', '--allow-empty',
                          '-m', 'Initial commit', cwd=repo)
            self.repos[alias] = repo
        self.destination = self.root / 'tasks' / 'sample'
        self.arguments = [
            str(SCRIPT), 'sample', '--workspace-root', str(self.destination.parent), '--yes',
        ]
        for alias, repo in self.repos.items():
            self.arguments.extend(['--repo', f'{alias}={repo}'])
        self.addCleanup(self.remove_worktrees)

    def remove_worktrees(self):
        for alias, repo in self.repos.items():
            worktree = self.destination / 'src' / alias
            if worktree.exists():
                workspace.git('worktree', 'remove', '--force', worktree, cwd=repo)

    def run_main(self):
        with mock.patch.object(sys, 'argv', self.arguments):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                workspace.main()

    def test_creates_worktrees_under_src_and_metadata_at_root(self):
        self.run_main()
        task = (self.destination / 'CURRENT_TASK.md').read_text()
        self.assertFalse((self.destination / 'TASK.md').exists())
        self.assertIn('# Task: sample', task)
        self.assertNotIn('{{', task)
        for alias, repo in self.repos.items():
            worktree = self.destination / 'src' / alias
            self.assertTrue((worktree / '.git').is_file())
            self.assertFalse((self.destination / alias).exists())
            self.assertIn(f'`src/{alias}/`', task)
            self.assertEqual(workspace.git('branch', '--show-current', cwd=worktree),
                             'task/sample')
            self.assertEqual(workspace.git('rev-parse', 'HEAD', cwd=worktree),
                             workspace.git('rev-parse', 'HEAD', cwd=repo))
            self.assertEqual(workspace.git('status', '--porcelain', cwd=repo), '')
        for filename in ('AGENTS.md', 'CURRENT_TASK.md', 'WORKLOG.md'):
            self.assertTrue((self.destination / filename).is_file())
        instructions = (self.destination / 'AGENTS.md').read_text()
        self.assertIn('# Capsule workspace agent instructions', instructions)
        self.assertTrue((self.destination / '.github' / 'skills').is_dir())

    def test_rolls_back_nested_worktrees_when_creation_fails(self):
        original_git = workspace.git

        def fail_second_worktree(*args, **kwargs):
            if 'worktree' in args and 'add' in args and args[-2].name == 'frontend':
                raise subprocess.CalledProcessError(1, ['git', 'worktree', 'add'])
            return original_git(*args, **kwargs)

        with mock.patch.object(workspace, 'git', side_effect=fail_second_worktree):
            with self.assertRaises(subprocess.CalledProcessError):
                self.run_main()
        for alias, repo in self.repos.items():
            self.assertFalse((self.destination / 'src' / alias).exists())
            self.assertEqual(workspace.git('branch', '--list', 'task/sample', cwd=repo), '')
            registrations = workspace.git('worktree', 'list', '--porcelain', cwd=repo)
            self.assertEqual(registrations.count('worktree '), 1)

    def test_existing_branch_is_rejected_before_creating_workspace(self):
        workspace.git('branch', 'task/sample', cwd=self.repos['frontend'])
        with self.assertRaises(SystemExit) as error:
            self.run_main()
        self.assertEqual(error.exception.code, 2)
        self.assertFalse(self.destination.exists())
        self.assertEqual(workspace.git('branch', '--list', 'task/sample',
                                       cwd=self.repos['api']), '')


class SkillLayoutTests(unittest.TestCase):
    def test_bootstrap_skill_uses_discoverable_layout_with_bundled_dependencies(self):
        root = SCRIPT.parent.parent
        skill_directory = root / '.github' / 'skills' / 'create-capsule'
        skill = (skill_directory / 'SKILL.md').read_text()
        self.assertTrue(skill.startswith('---\nname: create-capsule\n'))
        self.assertIn('description:', skill)
        self.assertEqual(skill_directory.parents[2], root)
        self.assertTrue((root / 'scripts' / 'create_capsule.py').is_file())
        self.assertTrue((root / 'template' / 'CURRENT_TASK.md').is_file())
        self.assertFalse((root / 'skills' / 'create-task-workspace' / 'SKILL.md').exists())
        self.assertFalse((root / '.github' / 'skills' / 'create-task-workspace' / 'SKILL.md').exists())
        self.assertFalse((root / 'scripts' / 'create_workspace.py').exists())

    def test_script_help_uses_capsule_branding(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'],
                                check=True, text=True, capture_output=True)
        self.assertIn('create_capsule.py', result.stdout)
        self.assertIn('Create a Capsule task workspace', result.stdout)


if __name__ == '__main__':
    unittest.main()
