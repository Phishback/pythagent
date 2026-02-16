import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from call_functions import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if (api_key == "NONE"):
    raise Exception("API_KEY NOT FOUND - CHECK ENV FILE")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

try:
    for iteration in range(20):
        res = client.models.generate_content(
	        model="gemini-2.5-flash",
            contents=messages,
	        config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT,
                temperature=0
            ),
        )
        if res.candidates:
            for candidate in res.candidates:
                messages.append(candidate.content)
    
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        if res.function_calls:
            function_results = []
            for i in res.function_calls:
                function_call_result = call_function(i, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("function_call_result.parts is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("function_response is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("function_response.response is None")

                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(res.text)
            break
    else:
        print("Error: Maximum iterations (20) reached without a final res from the model")
        exit(1)
except RuntimeError as error:
    print(error)
    print("res.usage_metadata property not found - potential API failure")

