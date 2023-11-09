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
    print("pylint go")
    
    custom_rcfile = "C:/Users/larry/OneDrive/Documents/compsci/CSC-390/.pylintrc"
    
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
    
    print(output_text)
    
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