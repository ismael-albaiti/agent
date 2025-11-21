import os

from dotenv.main import StrPath
from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to read from",
            ),
        },
    ),
)


def get_file_content(working_directory: StrPath, file_path: StrPath):
    try:
        current_path = os.path.join(working_directory, file_path)
        current_abspath = os.path.abspath(current_path)

        # print(current_path)
        # print(current_abspath)

        if not current_abspath.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(current_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(current_abspath, "r") as stream:
            file_content_string = stream.read(MAX_CHARS)

        if os.path.getsize(current_abspath) > MAX_CHARS:
            file_content_string += (
                f"[...File {file_path} truncated at {MAX_CHARS} characters]"
            )
        return file_content_string
    except Exception as error:
        return f"Error: {error}"
