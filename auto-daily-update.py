#!/usr/bin/env python3
import os
import subprocess

# Modify these variables
BACKEND_PATH = os.path.expanduser("~/gitclones/DocIndex/")
FRONTEND_PATH = os.path.expanduser("~/gitclones/DocIndex-front/")
AUTHOR = "Dacosa"

# Function to get git logs
def get_git_log(repo_path, author):
    try:
        result = subprocess.run(
            ["git", "log", "--author", author, "--all", "--since=midnight", "--pretty=format:%h %an %ad"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() if result.stdout else "No commits found."
    except subprocess.CalledProcessError as e:
        return f"Error fetching commits: {e}"

# Get commit logs
backend_log = get_git_log(BACKEND_PATH, AUTHOR)
frontend_log = get_git_log(FRONTEND_PATH, AUTHOR)

# Construct prompt
SYSTEM_PROMPT = f"""
You will be given a list of git commits in a frontend and backend repositories.

Write a summary of all commits made by {AUTHOR}. Don't go too much into technical details.

First add today's date (Weekday + Month day) and then a list of changes, all in spanish.

Example:

== Input given to you:

Commits in backend:
No commits found.
Commits in frontend:
commit dfc2c67c0c4444823dd0aa491c8f63227f9e1b19
Author: Blaz Korecic <blaz@niuro.io>
Date:   Thu Feb 27 15:09:06 2025 -0300

    docs: Add changes to CHANGELOG

    to squash

commit a535fa22e64b5800ff6e2f9d5e5231d156ebb88e
Author: Blaz Korecic <blaz@niuro.io>
Date:   Thu Feb 27 15:06:20 2025 -0300

    fix: temporarily remove document actions in document display view

commit a74b05420081da34a297ec3af2692dadbaf360b9
Author: Blaz Korecic <blaz@niuro.io>
Date:   Thu Feb 27 14:52:39 2025 -0300

    fix: temporarily remove (comment) unused columns in SearchResults

commit f5b0ea7db373efde8556f1dc7afd9585bf1a0d40
Author: Blaz Korecic <blaz@niuro.io>
Date:   Thu Feb 27 12:45:59 2025 -0300

    refactor: Refactor code in SearchResults for clarity, create global tag color hash cache, fix small bugs


commit a5f0bd7db373aabd8556d1bc7aab9585ff1d0e40
Author: Blaz Korecic <blaz@niuro.io>
Date:   Thu Feb 27 11:45:59 2025 -0300

    
    refactor: Move tag color hash generation to utils/ and create a global cache for them

== Your output:

Jueves 27
    * Removidas temporalmente algunas componentes que no están siendo usadas.
    * Arreglados bugs pequeños.
    * Refactor en SearchResults para mayor claridad.
    * Movido el hash de colores para etiquetas a `utils/` y creado un cache global para no recalcularlos.
"""

PROMPT = """
Commits in backend repository (DocIndex):
{backend_log}

Commits in frontend repository (DocIndex-front):
{frontend_log}
"""



# Print commit logs (for debugging)
print("Commits in backend:")
print(backend_log)
print("Commits in frontend:")
print(frontend_log)

# Run llm with the constructed prompt
try:
    result = subprocess.run(["llm", "prompt", "-s", SYSTEM_PROMPT, PROMPT], capture_output=True, text=True, check=True)
    print("\nLLM Response:\n")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error running llm: {e}")
