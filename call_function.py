
from types import FunctionType
from google.genai import types

from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def call_function(function_call_part: types.FunctionCall, verbose:bool=False):
    function_name = function_call_part.name
    if not function_name:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="None",
                    response={"error": "function name was not provided"},
                )
            ],
        )

    function_arguments = function_call_part.args
    if not function_arguments:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="None",
                    response={"error": "function arguments was not provided"},
                )
            ],
        )

    if verbose:
        print(f" - Calling function: {function_name}({function_arguments})")
    else: 
        print(f" - Calling function: {function_name}")

    function_map: dict[str, FunctionType] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_result:str = function_map[function_name](
        WORKING_DIRECTORY, **function_arguments) 

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
