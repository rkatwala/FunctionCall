import openai
import json
# Your OpenAI API key
openai.api_key = ''

# Define the function
def sum_numbers(a, b):
    return a + b

# User's input query
user_query = "What is the sum of 5 and 7?"
messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_query}
        ]
# Call the OpenAI API with the user's query
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[
        {   
            "type": "function",
            "function": {
                "name": "sum_numbers",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "a": {
                            "type": "integer"

                        },

                        "b": {
                            "type": "integer"
                        }
                    }
                    
                }
            }
        }
    ]
)

# Get the function call result
response_message = response.choices[0].message
tool_calls = response_message.tool_calls
# Step 2: check if the model wanted to call a function
if tool_calls:
    # Step 3: call the function
    # Note: the JSON response may not always be valid; be sure to handle errors
    available_functions = {
        "sum_numbers": sum_numbers,
    }  # only one function in this example, but you can have multiple
    messages.append(response_message)  # extend conversation with assistant's reply
    # Step 4: send the info for each function call and function response to the model
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            a=function_args.get("a"),
            b=function_args.get("b"),
        )
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
    second_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )  # get a new response from the model where it can see the function response
    print(second_response)
