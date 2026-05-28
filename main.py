import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
# from functions.get_files_info import schema_get_files_info
from functions.call_functions import available_functions, call_function
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()






def call_llm(client, messages, config):
    response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=config
    )
    return response

def main():
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    user_prompt = args.user_prompt
    client = genai.Client(api_key=api_key)
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)

    for _ in range(20):
        response = call_llm(client, messages, config)
        if response.usage_metadata is None:
            raise RuntimeError("Failed API call ")
        else:
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            if args.verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(response.text)
            if response.function_calls:
                function_results = []
                for function_call in response.function_calls:
                    print(f"Calling function: {function_call.name}({function_call.args})")
                    function_call_result = call_function(function_call, args.verbose)
                    # 10.1 Check for empty parts
                    if not function_call_result.parts:
                        raise Exception("Function call result has no parts.")

                    # 10.2 Check for missing function_response
                    if function_call_result.parts[0].function_response is None:
                        raise Exception("Function call result has no function_response.")

                    # 10.3 Check for missing response data
                    if function_call_result.parts[0].function_response.response is None:
                        raise Exception("Function call result has no response data.")

                    # 10.4 Save the part to a list (assuming you have a list called 'function_results' initialized earlier)
                    function_results.append(function_call_result.parts[0])

                    # 10.5 Print the result if verbose is True
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response['result']}")

                messages.append(types.Content(role="user", parts=function_results))
            else:
                print(f"Response: {response.text}")
                return None
    print("Error: Reached maximum iterations (20) without a final response.")
    sys.exit(1)
    

if __name__ == "__main__":
    main()

