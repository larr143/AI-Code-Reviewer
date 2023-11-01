import openai
import os 

openai.api_key = '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'

messages = [ {"role": "system", 
"content": "You are a Intelligent Computer Science Program Tutor that reads python code and comments on the program on how to make the code more readable, better function nameing, refractoring, and better spacing. Also if the program won't run if ran comment on why it might not be running. Respond with the all of the code and the comments. Write the comments like the users are brand new to coding and need advice."} ]

print("Please enter the full path of your code that you want edited: ")

path = input('Path: ')

if os.path.splitext(path)[1] == ".py":
    with open(path, 'r') as f:
        code = f.read()
else: 
    print("you have attached a non Python file, please try again.")


if code:
    messages.append({"role": "user", "content": code},)
    chat = openai.ChatCompletion.create(model = 'gpt-3.5-turbo', messages=messages)
        
    reply = chat.choices[0].message.content
    print(f'ChatGPT: {reply}')