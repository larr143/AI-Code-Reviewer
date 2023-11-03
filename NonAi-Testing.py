from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import openai

openai.api_key = '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'


def main():
    
    # Custom open stream
    pylint_output = StringIO()

    # Create a reporter with the custom stream
    reporter = TextReporter(pylint_output)
    
    # Specify the path to your custom .pylintrc file
    custom_rcfile = "C:/Users/larry/Desktop/CSC 390/.pylintrc"
    
    code = "crapCode.py"

    # Run pylint on the specified file(s) with the custom reporter
    Run([code, "--rcfile", custom_rcfile], reporter=reporter, exit=False)

    # Retrieve the text report
    output_text = pylint_output.getvalue()
    
    # Split the output of pylint into a list 
    modified_output = output_text.splitlines()
    
    # deleting the first line that isnt needed
    modified_output.pop(0)
    
    # deleting all lines that arent codes
    for i in range(len(modified_output)):
        if "------------------------------" in modified_output[i]:
            del modified_output[i:]
            modified_output.pop()
            break

    for i in range(len(modified_output)):
        modified_output[i] = modified_output[i].lstrip(code)
     
     
    messages = [ {"role": "system", "content": 
        
    """
    Hello ChatGPT,

    I am working on a Python program aimed at helping new computer scientists understand their code better. 
    The program takes input code from users who are new to Python and runs pylint on it to identify issues.
    However, the output from pylint can be difficult for beginners to grasp due to its technical language and jargon.

    I need your assistance in making the pylint outputs more readable and user-friendly. 
    The goal is to generate clear and concise comments that explain the issues detected by pylint in a simple and easy-to-understand manner. 
    Imagine you are explaining these concepts to someone who is just starting to learn Python programming.
    I will give you the whole program from the student and individual errors codes for you to reword.
    
    Example pylint ouput for interpritation:
    :1:0: C0116: Missing function or method docstring (missing-function-docstring)
    1. The :1: is the line where pylint says the error is.
    2. The Second number inbetween colons in this example :0: doesnt mean anything in any case you will look at.
    3. The next part of the string that has one letter then 4 digits is the code C Means convention, W means Warning, E means Error. 
    4. After the last colon is the code description. 


    Here's two examples of the type of output you might encounter:
    
    Example Code:
    -----------
    def my_function(x):
        return x*2

    Pylint Output:
    --------------
    :12:0: W0612: Unused variable 'result' (unused-variable)

    Desired Comment:
    ---------------
    Warning: The variable 'result' is defined but not used in your code. In Python, it's important to remove any unused variables to keep your code clean and efficient.


    Example Code:
    -----------
    def calculate_area_of_rectangle(length, width):
        area= length*width
        return area
        
    Pylint Output:
    --------------
    :1:0: C0114: Missing module docstring (missing-module-docstring)
    
    Desired Comment:
    ---------------
    Convention: The function "calculate_area_of_rectangle" does not have a docstring, A docstring is a special type of comment in code that explains what a specific part of the code does, helping other developers (or the coder themselves) understand its purpose and how to use it.
    

    Please help me by rewording the pylint outputs like the example comment above. Your assistance will be invaluable in making the learning process smoother for new computer scientists. Thank you!

    Best regards,
    Larry Tieken
    """} ]


    file = open("C:/Users/larry/Desktop/CSC 390/crapCode.py", 'r')
    
    messages.append(
       {"role": "user", "content": file.read()}, 
    )
    
    for i in modified_output:
        if len(messages) > 2:
            messages.pop()

            messages.append(
                {"role": "user", "content": i}    
            )
        else:
            messages.append(
                {"role": "user", "content": i}    
            )
        
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
        
        reply = chat.choices[0].message.content 
    
        print(reply) 

    
    
    # for i in modified_output:
    #     print(i)
    
    

if __name__ == "__main__":
    main()
    
    
    
""" Output Docstring
Convention: Your code is missing a final newline at the end. Adding a final newline is a good practice as it ensures that the file ends with a blank line, which is the standard convention in Python.
Convention: The module does not have a docstring. A docstring is a special type of comment at the beginning of a Python file that explains its purpose and provides an overview of its content. Adding a docstring to your code helps other developers (or yourself) understand what the module does and how to use it.
Convention: The module name "crapCode" does not adhere to the recommended snake_case naming style. In Python, it is best practice to name modules using lowercase letters and underscores.
Convention: The function "calculate_area_of_rectangle" does not have a docstring. A docstring is a special type of comment in your code that explains what a specific part of the code does, helping other developers (or yourself) understand its purpose and how to use it. It is recommended to add a docstring to your function to improve code readability and maintainability.
Convention: The function "print_rectangle_properties" does not have a docstring. A docstring is a special type of comment in code that explains what a specific part of the code does, helping other developers (or the coder themselves) understand its purpose and how to use it.
Convention: The variable "length_of_rectangle" does not follow the recommended naming style. In Python, constants are typically written in uppercase letters with underscores between words. To improve the readability and maintainability of your code, consider renaming the variable to "LENGTH_OF_RECTANGLE".
Convention: The constant "width_of_rectangle" should be named using uppercase letters and underscores to follow the naming style convention for constants in Python. Consider renaming it to "WIDTH_OF_RECTANGLE" for better readability and adherence to the recommended naming convention.
"""
