import ast
import os
import tempfile
import tkinter as tk
import tkinter.messagebox
from io import StringIO
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.scrolledtext import ScrolledText

import openai
from pylint.lint import Run
from pylint.reporters.text import TextReporter


class windows(tk.Tk):
    
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Creating a dictionary of frames
        self.frames = {}
        
        #creating the variables that store code and the comments. 
        self.code = ""
        self.pylint_comments = []
        self.chatgpt_comments = [] 
        
        # Adding a title to the window
        self.wm_title("Code Reviewer")

        # creating a frame and assigning it to container
        container = tk.Frame(self, width=400,height=600)
        
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, CodeDisplayPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        # Creating a bind for when the size ofthe frame changes then sending the update size command to the frame.
        self.bind("<Configure>", self.frames[MainPage].update_size)
        self.prev_width = self.winfo_width()
        self.prev_height = self.winfo_height()     
        
        self.menu_bar()
        
        # Using a method to switch frames
        self.show_frame(MainPage)
    
    def menu_bar(self):
        
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open",
            command=self.frames[MainPage].user_file_selection)
        filemenu.add_command(label="Save",
            command=self.frames[CodeDisplayPage].save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index",
            command=self.help_dialog)
        helpmenu.add_command(label="About...",
            command=self.about_dialog)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.config(menu=menubar)
    
    def pylint_Processing(self, code):
        
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        temp_file_path = os.path.join(temp_dir, 'temp_script.py')  # Create a temporary file path

        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(code)  # Write the input string to the temporary file
    
        custom_rcfile = "C:/Users/larry/OneDrive/Documents/compsci/CSC-390/.pylintrc"
    
        # Custom open stream
        pylint_output = StringIO()

        # Create a reporter with the custom stream
        reporter = TextReporter(pylint_output)
    
        # Specify the path to your custom .pylintrc file
        custom_rcfile = "C:/Users/larry/OneDrive/Documents/compsci/CSC-390/.pylintrc"
        
        # Run pylint on the specified file(s) with the custom reporter
        Run([temp_file_path, "--rcfile", custom_rcfile],
            reporter=reporter, exit=False)

        # Retrieve the text report
        output_text = pylint_output.getvalue()
    
        # Split the output of pylint into a list
        modified_output = output_text.splitlines()
        
        # deleting the first line that isnt needed
        modified_output.pop(0)
        
        for i in range(len(modified_output)):
            if "------------------------------" in modified_output[i]:
                del modified_output[i:]
                modified_output.pop()
                break

        for i in range(len(modified_output)):
            modified_output[i] = modified_output[i].replace((temp_file_path + ':') , '')
            
        self.pylint_comments = modified_output
            
    def show_frame(self, cont):
        frame = self.frames[cont]
        
        if cont is CodeDisplayPage: frame.text_Population()
        
        # raises the current frame to the top
        frame.tkraise()

    def on_resize(self, event):
        # Get the new size of the window
        width = event.width
        height = event.height

        # Check if the size has actually changed
        if width != self.prev_width or height != self.prev_height:
            self.prev_width = width
            self.prev_height = height

            # Resize components accordingly
            for frame in self.frames.values():
                frame.update_size(width, height)
    
    def help_dialog(self):
        message = """
If you are having troubles with entering your code into the entry box.
	- Make sure the code is properly indented, if the function you enter 
	starts with a tab or spaces infront of it, it isn't properly indented
	- For example, the first main is correct the second is tabbed wrong.
def main():
	print("Hello World!")

	def main():
		print("Hello World!")

If all of that isn't working you can use the open button on the menu in the home winow to add your code directly from a python file. 
        """
        
        tkinter.messagebox.showinfo("Help", message)
    
    def about_dialog(self):
        message = """
This program is a Code reviewer that takes in any size of python program.
It will then pass that program to Pylint, once Pylint reports, the reports are then sent to ChatGPT. 
ChatGPT will then reword the reports to help new users understand the problems with the program. 
This includes errors, warnings, convention, and refactoring. 

This program was written by Larry Tieken. 
        """
        
        tkinter.messagebox.showinfo("Help", message)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.isvalid = None
        self.what_to_display()
        
    def what_to_display(self):
        
        self.clear_page()
        
        ttk.Label(self, text="Welcome! Please input your code below, then click the next button!", 
            font=("Times New Roman", 18), background="#121841",
            foreground="#C93D4F").grid(column=0, row=0, padx=2, pady=2)
      
               
        self.text_area = tk.Text(self, wrap=tk.NONE, 
            width=60, height=18, font=("Consolas", 12)) 

        self.text_area.grid(column=0, row=1, pady=2,
            padx=2, sticky="nsew")
        
        scrolly = ttk.Scrollbar(self, command=self.text_area.yview)
        scrolly.grid(row=1, column=1, sticky='nsew')
        self.text_area['yscrollcommand'] = scrolly.set
            
        scrollx = ttk.Scrollbar(self, orient="horizontal",
            command=self.text_area.xview)
        scrollx.grid(row=2, column=0, sticky='nsew')
        self.text_area['xscrollcommand'] = scrollx.set
        
        
        if type(self.isvalid) == bool:
            if not self.isvalid:
                validtext = tk.Label(self, 
                    text="your code is not valid, please try again!")
                validtext.grid(column=0, row=4, 
                    pady=10, padx=10, sticky="nsew")
            else: 
                validtext = tk.Label(self, text="")
                validtext.grid(column=0, row=4,
                    pady=10, padx=10, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1) 
        
        self.button = tk.Button(
            self,
            text="Next(Might take a second)",
            command=lambda: self.code_Checker()
        )
        self.button.grid(column=0, row=3, pady=5, padx=5)  
        
        self.frame_style()
        
    def user_file_selection(self):
        
        file = filedialog.askopenfile(mode='r',
            filetypes=[('Python Files', '*.py')])

        if file:
            # Read the content from the file object
            content = file.read()

            # Insert the content into the text area
            self.text_area.insert(tk.END, content)

            # Close the file
            file.close()
        
        self.update_idletasks()   
        
    def frame_style(self):
        
        self.text_area.config(undo=True, background="#262335",
            borderwidth=3, relief="sunken", foreground="#F573C8") 
        
        style=ttk.Style()
        style.theme_use('classic')
        style.configure("Vertical.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
        style.configure("Horizontal.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
        
        
        self.button.config(background="#241B2F", 
            foreground="#C93D4F")
        
        
        self.config(bg='#121841')
    
    def code_Checker(self):
        try:
            ast.parse(self.text_area.get('1.0', 'end-1c'))
            self.isvalid = True
        except SyntaxError:
            self.isvalid = False
            self.what_to_display()
        
        if self.isvalid == True:
            self.isvalid = True
            self.controller.code = self.text_area.get("1.0", "end-1c")
            self.controller.pylint_Processing(self.controller.code)
            self.chatgpt_Processing()

    def chatgpt_Processing(self):
        
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

        
        for i in self.controller.pylint_comments:
            
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
            
            self.controller.chatgpt_comments.append(reply)
        
        self.controller.show_frame(CodeDisplayPage)
         
    def update_size(self, event):
        # Get the new size of the frame
        width = event.width
        height = event.height

        # Resize the text area accordingly
        self.text_area.config(width=width // 10, height=height // 30)
        
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
     
        
class CodeDisplayPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.code_Display = tk.Text(self, wrap=tk.NONE, 
                width=60, height=20, font=("Consolas", 12))
        
        self.text_Population
        
    def text_Population(self):
        
        self.clear_page
        
        if len(self.controller.chatgpt_comments) > 0: 
            # ensure a consistent GUI size
            self.grid_propagate(False)
            
            ttk.Label(self, text="Here Is your code!", 
            font=("Times New Roman", 18), background="#121841",
            foreground="#C93D4F").grid(column=0, row=0, padx=2, pady=2)
            
        
            self.code_Display = tk.Text(self, wrap=tk.NONE, 
                width=60, height=20, font=("Consolas", 12))
            
            self.code_Display.grid(column=0, row=1, pady=2,
                padx=2, sticky="nsew")
            
            scrolly = ttk.Scrollbar(self, command=self.code_Display.yview)
            scrolly.grid(row=1, column=1, sticky='nsew')
            self.code_Display['yscrollcommand'] = scrolly.set
            
            scrollx = ttk.Scrollbar(self, orient="horizontal" ,
                command=self.code_Display.xview)
            scrollx.grid(row=2, column=0, sticky='nsew')
            self.code_Display['xscrollcommand'] = scrollx.set
            
            self.code_Display.config(undo=True)
            self.code_Display.config(borderwidth=3, relief="sunken")
            
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)
            
            code_list = self.controller.code.splitlines()
            error_line_numbers = []
            line_Number = 0
            error_index = 0
            code_with_comments = []
            
            for i in self.controller.pylint_comments:
                digit = 0 
                number = ""
                for j in range(len(i)):
                    if i[j].isdigit():
                        number += i[j]
                        digit = digit + 1
                    elif i[j] == ':':
                        error_line_numbers.append(number)
                        break
                    
                    
            for i in code_list:
            
                for j in error_line_numbers:
                
                    if int(j) == line_Number:   
                        code_with_comments.append(self.controller.chatgpt_comments[error_index])
                        error_index += 1
                    else:
                        error_index += 1
                    
                error_index = 0
                code_with_comments.append(i)
                line_Number += 1
            
            for line in code_with_comments:
                self.code_Display.insert(tk.END, line + "\n")

            self.frame_style()
            
            self.update_idletasks()
            
    def frame_style(self):
        
        self.code_Display.config(undo=True, background="#262335", 
            borderwidth=3, relief="sunken", foreground="#F573C8")
        
        
        style=ttk.Style()
        style.theme_use('classic')
        style.configure("Vertical.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
        style.configure("Horizontal.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
            
        self.config(bg='#121841')   
        
    def save(self):
        if len(self.code_Display.get('1.0', 'end-1c')) > 0:
            f = asksaveasfile(initialfile = 'CommentedCode.txt',
                defaultextension=".txt", filetypes=[("All Files","*.*")])
            code = self.code_Display.get('1.0', 'end-1c')
            f.write(code)
            f.close
    
    def update_size(self, event):
        # Get the new size of the frame
        width = event.width
        height = event.height

        # Resize the text area accordingly
        self.code_Display.config(width=width // 10, height=height // 30) 
          
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
        


if __name__ == "__main__": 
    
    api_key_file = open("C:/Users/larry/OneDrive/Desktop/API KEY.txt", 'r')
    openai.api_key = api_key_file.read()
    
    testObj = windows()
    testObj.geometry("800x600")
    testObj.mainloop()