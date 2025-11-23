import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import Client, types

from call_function import available_functions, call_function
from config import MAX_ITERATIONS
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
    verbose: bool = args.verbose

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_prompt),
            ],
        ),
    ]

    for i in range(MAX_ITERATIONS):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                sys.exit(0)
                # break
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
    sys.exit(1)


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

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    responses: list[types.Part] = []
    for function_call_part in response.function_calls:
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

    messages.append(
        types.Content(
            role="user",
            parts=responses,
        ),
    )


if __name__ == "__main__":
    main()
