import os
import sys


def get_project_root():
    """Returns the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # avoid recursive search for root folder
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    if os.path.exists(os.path.join(project_root, 'config', 'config.yaml')):
        return project_root
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, 'config', 'config.yaml')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None


project_root = get_project_root()

if project_root is None:
    raise RuntimeError("Project root not found. Ensure the script is placed correctly within the project structure.")

if project_root not in sys.path:
    sys.path.append(project_root)
