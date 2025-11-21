import os

from dotenv.main import StrPath
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write content to a file and save it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to create and write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write into the file",
            ),
        },
    ),
)


def write_file(working_directory: StrPath, file_path: StrPath, content: str) -> str:
    try:
        current_path = os.path.join(working_directory, file_path)
        current_abspath = os.path.abspath(current_path)
        current_dirname = os.path.dirname(current_abspath)

        # print(current_path)
        # print(current_abspath)

        if not current_abspath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # if not os.path.isfile(current_abspath):
        # return f'Error: File not found or is not a regular file: "{file_path}"'

        if not os.path.exists(current_dirname):
            os.makedirs(current_dirname)

        with open(current_abspath, "w") as stream:
            _ = stream.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as error:
        return f"Error: {error}"
