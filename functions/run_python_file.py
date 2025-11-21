import os
import subprocess

from dotenv.main import StrPath
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="a function to run a python file within the working_directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the python file to run",
            ),
            "args": types.Schema(
                type=types.Type.TYPE_UNSPECIFIED,
                description="extra args to add to when running the file",
            ),
        },
    ),
)


def run_python_file(working_directory: StrPath, file_path: str, args=[]):
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    current_path = os.path.join(working_directory, file_path)
    current_abspath = os.path.abspath(current_path)

    # print(current_path)
    # print(current_abspath)

    if not os.path.isfile(current_abspath):
        return f'Error: File "{file_path}" not found.'
    if not current_abspath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    try:
        result = subprocess.run(
            args=["python", current_abspath] + args, timeout=30, capture_output=True
        )

        if len(result.stdout) == 0:
            return "No output produced."

        report = f"STDOUT:{result.stdout} \nSTDERR:{result.stderr}"
        if result.returncode != 0:
            report += f"\nProcess exited with code {result.returncode}\n"

            report += "\nNo output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return report
