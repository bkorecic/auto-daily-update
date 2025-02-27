#!/usr/bin/env python3
import os
import subprocess

# Modify these variables
BACKEND_PATH = os.path.expanduser("~/gitclones/DocIndex/")
FRONTEND_PATH = os.path.expanduser("~/gitclones/DocIndex-front/")
AUTHOR = "Blaz"

# Function to get git logs
def get_git_log(repo_path, author):
    try:
        # Run git log command
        result = subprocess.run(
            ["git", "log", "--author", author, "--all", "--since=midnight", "--pretty=format:COMMIT:%n%s%n%b%n", "--no-merges"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split commits and filter out those with "Co-authored-by:"
        commits = result.stdout.strip().split("\nCOMMIT:")
        filtered_commits = [commit for commit in commits if "Co-authored-by:" not in commit]
        
        # Rejoin with "COMMIT:" prefix to maintain formatting
        output = "\nCOMMIT:".join(filtered_commits)

        return output if output else "No commits found."
    
    except subprocess.CalledProcessError as e:
        return f"Error fetching commits: {e}"

# Get commit logs
backend_log = get_git_log(BACKEND_PATH, AUTHOR)
frontend_log = get_git_log(FRONTEND_PATH, AUTHOR)

# Construct prompt
SYSTEM_PROMPT = """
You will be given a list of Git commits from frontend and backend repositories.

Your task is to generate a concise summary of all the commits, avoiding excessive technical details.

### Instructions:
- Begin with today's date in Spanish, formatted as: **"Weekday Day"** (e.g., "Jueves 27").
- Summarize the changes in bullet points.
- Keep the descriptions clear and high-level, avoiding unnecessary implementation details.
- If there are no commits in a repository, do not mention it.

### Example:

#### Input:

Commits in backend:
No commits found.

Commits in frontend:
COMMIT:
docs: Add changes to CHANGELOG
to squash


COMMIT:
fix: temporarily remove document actions in document display view


COMMIT:
fix: temporarily remove (comment) unused columns in SearchResults


COMMIT:
refactor: Refactor code in SearchResults for clarity, create global tag color hash cache, fix small bugs



#### Expected Output:

Jueves 27
    * Removidas temporalmente algunas componentes que no están siendo usadas.
    * Arreglados bugs pequeños.
    * Refactor en SearchResults para mayor claridad.
    * Movido el hash de colores para etiquetas a `utils/` y creado un cache global para no recalcularlos.
"""

PROMPT = f"""
Commits in backend repository:
{backend_log}

Commits in frontend repository:
{frontend_log}
"""

# Run llm with the constructed prompt
try:
    result = subprocess.run(["llm", "prompt", "-s", SYSTEM_PROMPT, PROMPT], capture_output=True, text=True, check=True)
    print("\nLLM Response:\n")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error running llm: {e}")
