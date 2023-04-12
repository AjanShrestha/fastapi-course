1. Virtual Environments

   - Example:
     - Project 1
       - Fastapi v1.2.3
       - System -> Fastapi v1.2.3
     - Project 2
       - Fast api v2.4.5
       - System -> Upgrade to v 2.4.5?
         - Is it backward compatible
   - Venv example:
     - Project 1
       - Venv1
         - Fastapi v1.2.3 -> Isolated
     - Project 2
       - Venv 2
         - Fast api v2.4.5 -> Isolated
     - System -> Doesn't pollute it
   - Virtual environment provide a fresh, isolated environment for libraries and frameworks to exist without polluting the global environment
   - Command
     ```bash
         python3 -m venv <name>
     ```
   - Activate Command
     ```bash
         source ./venv/bin/activate
     ```
   - VSCode -> Select the interpreter

2. Run command

   - ```bash
         uvicorn main:app
     ```
   - `main`: the file `main.py`(the Python "module")
   - `app`: the object created inside of `main.py` with the line `app = FastAPI`
   - `--reload`: makes the server restart after code changes. Only use for development.
