import os
from pathlib import Path

def create_project_structure(base_path: str):
    """
    Creates the directory structure for the webvoyager_self_improvement_framework.

    Args:
        base_path: The root directory where the structure should be created.
                   This would be the root of your new Git repository.
    """
    base_dir = Path(base_path)

    # Define the core directories relative to the base_dir
    directories = [
        ".github/workflows",
        "core",
        "agents",
        "evaluation/docker",
        "evaluation/data/webbench", # Placeholder for webbench data
        "scripts",
        "experiments",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "docs",
        "venv", # Will be ignored by Git, but good to create
    ]

    print(f"Creating directory structure under: {base_dir}")

    for path_str in directories:
        dir_path = base_dir / path_str
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {dir_path}")
        except Exception as e:
            print(f"Error creating {dir_path}: {e}")

    # Create dummy .gitkeep files to ensure empty directories are committed
    # Git doesn't track empty directories, so .gitkeep is a common workaround.
    gitkeep_dirs = [
        ".github/workflows",
        "core",
        "agents",
        "evaluation/data/webbench",
        "scripts",
        "experiments",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "docs",
    ]

    for path_str in gitkeep_dirs:
        gitkeep_file = base_dir / path_str / ".gitkeep"
        if not gitkeep_file.exists():
            try:
                gitkeep_file.touch()
                print(f"Created .gitkeep in: {gitkeep_file.parent}")
            except Exception as e:
                print(f"Error creating .gitkeep in {gitkeep_file.parent}: {e}")

    print("\nDirectory structure creation complete.")
    print("Remember to add a .gitignore, requirements.txt, README.md, and LICENSE manually.")


if __name__ == "__main__":
    # Example usage:
    # This will create the structure in a subdirectory named 'my_framework_repo'
    # in the current working directory where you run the script.
    
    # You might want to change this to an absolute path if running from a specific context.
    # For example:
    # root_directory = "/path/to/your/new/framework/repo"
    
    root_directory_name = "webvoyager_self_improvement_framework"
    create_project_structure(root_directory_name)

    # After running this script, you would then:
    # 1. cd webvoyager_self_improvement_framework
    # 2. git init .
    # 3. git add .
    # 4. git commit -m "Initial framework structure"
    # 5. Connect to your remote GitHub repo and push.