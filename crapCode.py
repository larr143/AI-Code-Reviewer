from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import os
import tempfile

def create_temp_python_file(code):
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    temp_file_path = os.path.join(temp_dir, 'temp_script.py')  # Create a temporary file path

    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)  # Write the input string to the temporary file

    pylint_Processing(temp_file_path)  #Call pylint with the path of the temporary file


def pylint_Processing(path):
    
    # Custom open stream
    pylint_output = StringIO()

    # Create a reporter with the custom stream
    reporter = TextReporter(pylint_output)
    
    # Specify the path to your custom .pylintrc file
    custom_rcfile = "C:/Users/larry/OneDrive/Documents/compsci/CSC-390/.pylintrc"

    # Run pylint on the specified file(s) with the custom reporter
    Run([path, "--rcfile", custom_rcfile], reporter=reporter, exit=False)

    # Retrieve the text report
    output_text = pylint_output.getvalue()
    
    modified_output = output_text.splitlines()
        
    # deleting the first line that isnt needed
    modified_output.pop(0)
        
    for i in range(len(modified_output)):
        if "------------------------------" in modified_output[i]:
            del modified_output[i:]
            modified_output.pop()
            break

    for i in range(len(modified_output)):
        modified_output[i] = modified_output[i].replace( (path + ':') , '')
    
    
    error_line_numbers = []
        
    for i in modified_output:
        digit = 0 
        number = ""
        for j in range(len(i)):
            if i[j].isdigit():
                number += i[j]
                digit = digit + 1
            elif i[j] == ':':
                error_line_numbers.append(number)
                break
    
    code_list = code.splitlines()
    line_Number = 0
    error_index = 0
    code_with_comments = []
    
    for i in code_list:
        
        for j in error_line_numbers:
            
            if int(j) == line_Number:
                print(int(j), " ", error_index)    
                code_with_comments.append(modified_output[error_index])
                error_index += 1
            else:
                error_index += 1
                
        error_index = 0
        code_with_comments.append(i)
        line_Number += 1
    
    for i in code_with_comments:
        print(i)
        
    
if __name__ == "__main__":
    
    code ='''
def calculate_area_of_rectangle(length, width):
    area= length*width
    return area

def print_rectangle_properties(length,width):
    print("Length of rectangle: ",length)
    print("Width of rectangle: ", width)
    print("Area: ", calculate_area_of_rectangle(length,width))

length_of_rectangle=10
width_of_rectangle=5

print_rectangle_properties(length_of_rectangle,width_of_rectangle)
'''
    
    create_temp_python_file(code)