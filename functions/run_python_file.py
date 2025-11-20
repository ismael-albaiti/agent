import os
import subprocess

from dotenv.main import StrPath


def run_python_file(working_directory: StrPath, file_path: str, args=[]):
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    current_path = os.path.join(working_directory, file_path)
    current_abspath = os.path.abspath(current_path)
    # current_dirname = os.path.dirname(current_abspath)

    # print(current_path)
    # print(current_abspath)

    if not os.path.isfile(current_abspath):
        return f'Error: File "{file_path}" not found.'
    if not current_abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    try:
        a = subprocess.run(
            args=["python", current_abspath] + args, timeout=30, capture_output=True
        )
        report = f"STDOUT:{a.stdout}\nSTDERR:{a.stderr}\n"
        if a.returncode != 0:
            report += f"Process exited with code {a.returncode}\n"
        else:
            report += "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return report
