import subprocess
import shutil
from pathlib import Path
from typing import Optional

class GitManager:
    """
    Manages Git operations for the webvoyager_ev repository.
    """
    def __init__(self, webvoyager_repo_url: str, local_repo_dir: Path):
        """
        Initializes the GitManager.

        Args:
            webvoyager_repo_url: The URL of the webvoyager_ev GitHub repository.
            local_repo_dir: The local directory where the webvoyager_ev repo should be cloned/managed.
        """
        self.webvoyager_repo_url = webvoyager_repo_url
        self.local_repo_dir = local_repo_dir
        self.local_repo_dir.mkdir(parents=True, exist_ok=True) # Ensure parent directories exist

    def _run_git_command(self, command: list[str], cwd: Optional[Path] = None) -> str:
        """
        Internal helper to run a Git command and capture its output.

        Args:
            command: List of strings representing the Git command and its arguments.
            cwd: The current working directory for the command. Defaults to local_repo_dir.

        Returns:
            The stdout of the command.

        Raises:
            subprocess.CalledProcessError: If the Git command fails.
        """
        if cwd is None:
            cwd = self.local_repo_dir

        full_command = ["git"] + command
        print(f"Running Git command: {' '.join(full_command)} in {cwd}")

        result = subprocess.run(
            full_command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True  # Raise CalledProcessError if the command returns a non-zero exit code
        )
        return result.stdout.strip()

    def clone_or_pull(self, branch: str = "main"):
        """
        Clones the webvoyager_ev repository if it doesn't exist locally,
        otherwise pulls the latest changes for the specified branch.
        """
        if not self.local_repo_dir.exists() or not (self.local_repo_dir / ".git").is_dir():
            print(f"Cloning {self.webvoyager_repo_url} into {self.local_repo_dir}...")
            # For cloning with SSH, use ssh://git@github.com/... or just git@github.com:...
            # For PAT, it might be https://oauth2:YOUR_PAT@github.com/...
            self._run_git_command(["clone", self.webvoyager_repo_url, str(self.local_repo_dir)], cwd=self.local_repo_dir.parent)
        else:
            print(f"Repository already exists at {self.local_repo_dir}. Pulling latest changes...")
            self._run_git_command(["checkout", branch])
            self._run_git_command(["pull", "origin", branch])
        print(f"Successfully updated to branch '{branch}'.")

    def checkout(self, ref: str):
        """
        Checks out a specific branch or commit hash.
        """
        print(f"Checking out {ref}...")
        self._run_git_command(["checkout", ref])
        print(f"Successfully checked out '{ref}'.")

    def create_and_checkout_branch(self, branch_name: str, base_branch: str = "main"):
        """
        Creates a new branch from a base branch and checks it out.
        """
        self._run_git_command(["checkout", base_branch])
        try:
            self._run_git_command(["checkout", "-b", branch_name])
            print(f"Created and checked out new branch: {branch_name}")
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                print(f"Branch '{branch_name}' already exists. Checking it out instead.")
                self._run_git_command(["checkout", branch_name])
            else:
                raise

    def commit_and_push(self, message: str, branch: str = "main"):
        """
        Adds all changes, commits, and pushes to the specified branch.
        """
        print("Adding all changes...")
        self._run_git_command(["add", "."])
        print(f"Committing with message: '{message}'")
        self._run_git_command(["commit", "-m", message])
        print(f"Pushing to branch: {branch}")
        self._run_git_command(["push", "origin", branch])
        print("Changes pushed successfully.")

    def get_current_commit_hash(self) -> str:
        """
        Returns the current commit hash of the local repository.
        """
        return self._run_git_command(["rev-parse", "HEAD"])

    def get_diff(self, old_ref: str, new_ref: str = "HEAD") -> str:
        """
        Generates a Git diff between two references.
        """
        return self._run_git_command(["diff", old_ref, new_ref])

    def clean_repo(self):
        """
        Resets the repository to a clean state, discarding local changes.
        Useful before pulling or switching branches to avoid conflicts.
        """
        print(f"Cleaning repository: {self.local_repo_dir}")
        self._run_git_command(["reset", "--hard", "HEAD"])
        self._run_git_command(["clean", "-df"])
        print("Repository cleaned.")

    def delete_branch(self, branch_name: str, force: bool = False):
        """
        Deletes a local and remote branch.
        """
        print(f"Deleting local branch: {branch_name}")
        try:
            self._run_git_command(["branch", "-D" if force else "-d", branch_name])
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not delete local branch {branch_name}: {e.stderr.strip()}")

        print(f"Deleting remote branch: {branch_name}")
        try:
            self._run_git_command(["push", "origin", "--delete", branch_name])
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not delete remote branch {branch_name}: {e.stderr.strip()}")