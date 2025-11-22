import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import Client, types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "message",
        help="message to send to the agent",
        type=str,
    )
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose output",
    )

    args = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt: str = args.message
    if args.verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_prompt),
            ],
        ),
    ]

    generate_content(client, messages, args.verbose)


def generate_content(client: Client, messages: list[types.Content], verbose: bool):
    model = "gemini-2.0-flash-001"
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        responses = []
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Fatal: no response from function")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        responses.append(function_call_result.parts[0])

        if not responses:
            raise Exception("no function responses generated, exiting.")


# def call_function(function_call_part: types.FunctionCall, verbose=False):
#     function_name = function_call_part.name
#     if not function_name:
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name="None",
#                     response={"error": "function name was not provided"},
#                 )
#             ],
#         )
#
#     function_arguments = function_call_part.args
#     if not function_arguments:
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name="None",
#                     response={"error": "function arguments was not provided"},
#                 )
#             ],
#         )
#
#     if verbose:
#         print(f"Calling function: {function_name}({function_arguments})")
#     print(f" - Calling function: {function_name}")
#
#     functions: dict[str, FunctionType] = {
#         "get_file_content": get_file_content,
#         "get_files_info": get_files_info,
#         "write_file": write_file,
#         "run_python_file": run_python_file,
#     }
#
#     if function_name not in functions:
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_name,
#                     response={"error": f"Unknown function: {function_name}"},
#                 )
#             ],
#         )
#
#     func = functions[function_name]
#     return types.Content(
#         role="tool",
#         parts=[
#             types.Part.from_function_response(
#                 name=function_name,
#                 response={"result": func(WORKING_DIRECTORY, **function_arguments)},
#             )
#         ],
#     )
#

if __name__ == "__main__":
    main()
