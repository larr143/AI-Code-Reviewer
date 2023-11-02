import openai


openai.api_key = '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'

messages = [ {"role": "system", "content": 
"""Analyzing Python Code Based on PEP-8 Standards.

You are a Python coding expert helping beginners. Your task is to review the provided Python program carefully. 
Follow these guidelines:

1. Check each line for PEP-8 violations.
2. Identify and comment on issues with code style, variable names, and function names.
3. Suggest refactoring when necessary.
4. Explain issues clearly, assuming the reader is new to coding.
5. Dont Comment on the lines that follow PEP8 guidelines. 
Return the code with comments explaining the identified problems."""} ]


file = open("C:/Users/larry/OneDrive/Documents/compsci/CSC390-Projects/crapCode.py", 'r')
    
message = file.read() 
    
if message: 
        
    messages.append( 
        {"role": "user", "content": message}, 
    ) 
        
    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", messages=messages 
    ) 

reply = chat.choices[0].message.content 
    
print(f"ChatGPT: {reply}") 