import argparse
import os
from types import FunctionType

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("message", help="message to send to the agent")
    _ = parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose output"
    )

    args = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    user_prompt: str = args.message
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.function_calls:
        responses = []
        for func in response.function_calls:
            function_call_result = call_function(func, args.verbose)

            if not function_call_result.parts[0].function_response.response:
                raise Exception("Fatal: no response from function")

            responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    print(response.text)

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part: types.FunctionCall, verbose=False):
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
        print(f"Calling function: {function_name}({function_arguments})")
    print(f" - Calling function: {function_name}")

    functions: dict[str, FunctionType] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    working_directory = "./calculator"
    func = functions[function_name]
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": func(working_directory, **function_arguments)},
            )
        ],
    )


if __name__ == "__main__":
    main()
