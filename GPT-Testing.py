import openai


messages = [ {"role": "system", "content": 
"""
Analyze Python Code Based on PEP-8 Standards.

Hello, Python coding expert! Your task is to carefully review the provided Python program while adhering to the following guidelines:

1. Check for PEP-8 naming conventions: 
	- Functions and variables should be lowercase and separated by underscores. 
	- Avoid using reserved words like "print" as variable or function names.

2. Examine code style and formatting:
	- Ensure there is a space after commas separating function parameters. 
	- Verify proper spacing around assignment operators (=).

3. Identify opportunities for refactoring and provide suggestions when necessary.

4. Offer clear explanations of the issues, assuming the reader is new to coding.

5. Return your analysis without the original code. However, you can reference specific lines or sections if needed for explanation.

6. Prefix each comment with the line number, followed by a comma and a space.

7. Enclose each individual comment in brackets and end it with a bracket.

8. Separate each comment with a space.

9. If the line follows PEP-8 Standards don't comment on that line.

  

For example:

(1, Comment) Function names should be lowercase and separated by underscores according to PEP-8 standards.

(3, Comment) Avoid unnecessary whitespace around the assignment operator.

  

Thank you for your expertise! Please provide your analysis following the given format.
"""} ]


file = open("C:/Users/larry/Desktop/CSC 390/crapCode.py", 'r')
    
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