import ast
import os
import tempfile
import threading
import tkinter as tk
import tkinter.messagebox
from io import StringIO
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.scrolledtext import ScrolledText
import queue

import openai
from pylint.lint import Run
from pylint.reporters.text import TextReporter


class windows(tk.Tk):
    """windows Classmethod to handle windows .

    This class is the base frame that handles the containing and switching of 
    other frames. It also handles the styling of the main frame, including
    the menus options and dialogs. 

    Attributes:
        frames: A dictionary for containing tkinter frames.
        code: A string that contains the user's inputted code.
        pylint_comments: A list that will contain the Pylint output on the user's code.
        chatgpt_comments: A list that will contain ChatGPT's reworded Pylint outputs.

    Args:
        tk ([tkinter]): [a reference to the root window of the Tkinter application]
    """
    
    def __init__(self, *args, **kwargs):
        """__init__ Initialize the Tk ."""
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.frames = {} 
        self.code = ""
        self.pylint_comments = []
        self.chatgpt_comments = [] 
        
        self.wm_title("Code Reviewer")
        container = tk.Frame(self, width=400,height=600)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Adding Windows to the dictionary.
        for F in (MainPage, CodeDisplayPage, LoadingPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        # Creating a bind for when the size of the frame changes then sending the update size command to the frame.
        self.bind("<Configure>", self.frames[MainPage].update_size)
        self.prev_width = self.winfo_width()
        self.prev_height = self.winfo_height()     
        
        self.menu_bar()
        self.show_frame(MainPage)
    
    def menu_bar(self):
        """menu_bar called to create the menubar ar the top of the program"""
        
        menuBar = tk.Menu(self)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open",
            command=self.frames[MainPage].user_file_selection)
        fileMenu.add_command(label="Save",
            command=self.frames[CodeDisplayPage].save)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="File", menu=fileMenu)
        
        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Help Index",
            command=self.help_dialog)
        helpMenu.add_command(label="About...",
            command=self.about_dialog)
        menuBar.add_cascade(label="Help", menu=helpMenu)
        
        self.config(menu=menuBar)
            
    def show_frame(self, cont):
        """show_frame Raises desired container

        Args:
            cont (Container): Contains the container the program wants to display.
        """
        frame = self.frames[cont]
        if cont is CodeDisplayPage: frame.text_Population()
        frame.tkraise()

    def on_resize(self, event):
        """on_resize resize components on window resize. 

        Args:
            event (ResizeEvent): The change in height and width of the program 
        """
        width = event.width
        height = event.height
        
        if width != self.prev_width or height != self.prev_height:
            self.prev_width = width
            self.prev_height = height
            
            for frame in self.frames.values():
                frame.update_size(width, height)
    
    def help_dialog(self):
        """help_dialog Creates help dialog when called"""        
        message = """
            If you are having troubles with entering your code into the entry box.
	            - Make sure the code is properly indented, if the function you enter 
	            starts with a tab or spaces in-front of it, it isn't properly indented
	            - For example, the first main is correct the second is tabbed wrong.
            def main():
	            print("Hello World!")

	            def main():
		            print("Hello World!")

            If all of that isn't working you can use the open button on the
            menu in the home window to add your code directly from a python file. 
        """
        
        tkinter.messagebox.showinfo("Help", message)
    
    def about_dialog(self):
        """about_dialog Creates about dialog when called"""        
        message = """
        This program is a Code reviewer that takes in any size of python program.
        It will then pass that program to Pylint, once Pylint reports, the reports are then sent to ChatGPT. 
        ChatGPT will then reword the reports to help new users understand the problems with the program. 
        This includes errors, warnings, convention, and refactoring. 

        This program was written by Larry Tieken. 
        """
        
        tkinter.messagebox.showinfo("Help", message)


class MainPage(ttk.Frame):
    """Container for the Main Page of the program.

    The main page is where users will be able to enter their code for review.
    
    Attributes: 
        isValid (Boolean): Contains a boolean on code validity.

    Args:
        ttk (Frame): Frame widget that contains other widgets using ttk for stylization.
    """
    
    def __init__(self, parent, controller):
        """__init__ Initializes the container and its widgets."""
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.isValid = None
        self.what_to_display()
        
    def what_to_display(self):
        """what_to_display Creates all of the widgets in the container and places them."""
        
        self.clear_page()
        
        ttk.Label(self, text="Welcome! Please input your code below, then click the next button!", 
            font=("Times New Roman", 18), background="#121841",
            foreground="#C93D4F").grid(column=0, row=0, padx=2, pady=2)
      
        self.text_area = tk.Text(self, wrap=tk.NONE, 
            width=60, height=18, font=("Consolas", 12)) 

        self.text_area.grid(column=0, row=1, pady=2,
            padx=2, sticky="nsew")
        
        scrollY = ttk.Scrollbar(self, command=self.text_area.yview)
        scrollY.grid(row=1, column=1, sticky='nsew')
        self.text_area['yscrollcommand'] = scrollY.set
            
        scrollX = ttk.Scrollbar(self, orient="horizontal",
            command=self.text_area.xview)
        scrollX.grid(row=2, column=0, sticky='nsew')
        self.text_area['xscrollcommand'] = scrollX.set
        
        # Creates a label if user input was not valid Python code.
        if type(self.isValid) == bool:
            if not self.isValid:
                validText = tk.Label(self, 
                    text="your code is not valid, please try again!")
                validText.grid(column=0, row=4, 
                    pady=10, padx=10, sticky="nsew")
            else: 
                validText = tk.Label(self, text="")
                validText.grid(column=0, row=4,
                    pady=10, padx=10, sticky="nsew")
        
        self.button = tk.Button(
            self,
            text="Next(Might take a second)",
            command=lambda: self.code_Checker()
        )
        self.button.grid(column=0, row=3, pady=5, padx=5)  
        
        self.frame_style()
        
    def user_file_selection(self):
        """user_file_selection 
        
        Creates file search dialog to find .py files.
        On user input inserts file contents into entry box for code review.
        """
        
        file = filedialog.askopenfile(mode='r',
            filetypes=[('Python Files', '*.py')])

        if file:
            content = file.read()
            self.text_area.insert(tk.END, content)
            file.close()
        
        self.update_idletasks()   
        
    def frame_style(self):
        """Styles the container and widgets."""
        
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
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1) 
        
        self.config(bg='#121841')
    
    def code_Checker(self):
        """Checks if user inputted code is valid using AST."""
        
        # A try except to check if the code entered is parsable python 
        try:
            ast.parse(self.text_area.get('1.0', 'end-1c'))
            self.isValid = True
        except SyntaxError:
            self.isValid = False
            self.what_to_display()
        
        if self.isValid == True:
            self.isValid = True
            self.controller.code = self.text_area.get("1.0", "end-1c")
            
            self.pylint_Processing()
            
            self.controller.frames[LoadingPage].start_processing()


    def pylint_Processing(self):
        """Runs Pylint on user inputted code then sets pylint_comments to Pylint output"""
        
        code = self.controller.code
        
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        temp_file_path = os.path.join(temp_dir, 'temp_script.py')  # Create a temporary file path
        
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(code)  # Write the input string to the temporary file
    
        pylint_output = StringIO()
        reporter = TextReporter(pylint_output)
        rcFile = "C:/Users/larry/OneDrive/Documents/compsci/CSC-390/.pylintrc"
        
        # Run pylint on the specified file(s) with the custom Pylint Config file. 
        Run([temp_file_path, "--rcfile", rcFile],
            reporter=reporter, exit=False)

        output_text = pylint_output.getvalue()
        modified_output = output_text.splitlines()# Split output into a list.
        modified_output.pop(0)# Deleting Pylint output title.
        
        #Gets rid of the Pylint score after the output Codes.
        for i in range(len(modified_output)):
            if "------------------------------" in modified_output[i]:
                del modified_output[i:]
                modified_output.pop()
                break

        #Gets rid of the input file path in-front of each code.
        for i in range(len(modified_output)):
            modified_output[i] = modified_output[i].replace((temp_file_path + ':') , '')
            
        self.controller.pylint_comments = modified_output

    # def chatgpt_Processing(self):
    #     """
    #     Takes Pylint output and sends it to ChatGPT to reword comments for new users. 
    #     ChatGPT is sent a priming message and the code for review along with individual 
    #     outputs from Pylint. This happens for each output from Pylint. Then sets chatgpt_comments equal 
    #     to the comments made by ChatGPT
    #     """
        
    #     #Creating a priming message as the system to tell ChatGPT how to respond
    #     #To the user 
    #     messages = [ {"role": "system", "content": """
    #     Hello ChatGPT,

    #     I am working on a Python program aimed at helping new computer scientists understand their code better. 
    #     The program takes input code from users who are new to Python and runs pylint on it to identify issues.
    #     However, the output from pylint can be difficult for beginners to grasp due to its technical language and jargon.

    #     I need your assistance in making the pylint outputs more readable and user-friendly. 
    #     The goal is to generate clear and concise comments that explain the issues detected by pylint in a simple and easy-to-understand manner. 
    #     Imagine you are explaining these concepts to someone who is just starting to learn Python programming.
    #     I will give you the whole program from the student and individual errors codes for you to reword.
    
    #     Example pylint output for interpretation:
    #     :1:0: C0116: Missing function or method docstring (missing-function-docstring)
    #     1. The :1: is the line where pylint says the error is.
    #     2. The Second number in-between colons in this example :0: doesn't mean anything in any case you will look at.
    #     3. The next part of the string that has one letter then 4 digits is the code C Means convention, W means Warning, E means Error. 
    #     4. After the last colon is the code description. 


    #     Here's two examples of the type of output you might encounter:
    
    #     Example Code:
    #     -----------
    #     def my_function(x):
    #         return x*2

    #     Pylint Output:
    #     --------------
    #     :12:0: W0612: Unused variable 'result' (unused-variable)

    #     Desired Comment:
    #     ---------------
    #     Warning: The variable 'result' is defined but not used in your code. In Python, it's important to remove any unused variables to keep your code clean and efficient.


    #     Example Code:
    #     -----------
    #     def calculate_area_of_rectangle(length, width):
    #         area= length*width
    #         return area
        
    #     Pylint Output:
    #     --------------
    #     :1:0: C0114: Missing module docstring (missing-module-docstring)
    
    #     Desired Comment:
    #     ---------------
    #     Convention: The function "calculate_area_of_rectangle" does not have a docstring, A docstring is a special type of comment in code that explains what a specific part of the code does, helping other developers (or the coder themselves) understand its purpose and how to use it.
    

    #     Please help me by rewording the pylint outputs like the example comment above. Your assistance will be invaluable in making the learning process smoother for new computer scientists. Thank you!

    #     Best regards,
    #     Larry Tieken
    #     """} ]

    #     #Sends ChatGPT a priming message, the user code, and pylint code 
    #     #For each code generated by Pylint. 
    #     for i in self.controller.pylint_comments:
            
    #         if len(messages) > 2:
    #             messages.pop()

    #             messages.append(
    #                 {"role": "user", "content": i}    
    #             )
    #         else:
    #             messages.append(
    #                 {"role": "user", "content": i}    
    #             )
        
    #         chat = openai.ChatCompletion.create( 
    #             model="gpt-3.5-turbo", messages=messages 
    #         )
            
    #         reply = chat.choices[0].message.content 
            
    #         self.controller.chatgpt_comments.append(reply)
        
    #     self.controller.show_frame(CodeDisplayPage)
         
    def update_size(self, event):
        """Resizes widgets in window when window is resized."""
        width = event.width
        height = event.height
        self.text_area.config(width=width // 10, height=height // 30)
        
    def clear_page(self):
        """clear_page Deletes all widgets in current container."""
        for widget in self.winfo_children():
            widget.destroy()
   
class LoadingPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.iteration = 0
        self.loading_label = ttk.Label(self, text="Processing...", font=("Times New Roman", 18))
        self.loading_label.pack(side="top",expand=True)
            
    def start_processing(self):
        self.controller.show_frame(LoadingPage)
        self.queue = queue.Queue()
        self.chat_thread = ChatGptThreaded(
            self.queue, self.controller.pylint_comments, self.controller.code
        )
        self.chat_thread.start()
        self.master.after(100, self.process_queue)  
    
    def process_queue(self):
        try:
            progress_info = self.queue.get_nowait()
            if isinstance(progress_info, dict):
                # Thread has completed, update UI accordingly
                self.loading_label.config(text="Processing completed.")
                self.controller.chatgpt_comments = progress_info["result"]
                self.controller.show_frame(CodeDisplayPage)
            elif isinstance(progress_info, int):
                # Update progress in the UI
                self.loading_label.config(text=f"Processing... {progress_info}%")
                self.update_idletasks()

            self.master.after(100, self.process_queue)

        except queue.Empty:
            if self.chat_thread.is_alive():
                self.master.after(100, self.process_queue)
    
    #def update_progress(self):
        
        # for i in self.controller.pylint_comments:
        #     self.progress.step(100/len(self.controller.pylint_comments))
        #     self.update_idletasks()
        #     threading.Thread(target=self.chatgpt_Processing, args=(i,)).start()
        #     self.iteration += 1 
        #     print("itter")
            
        # print("done")
        # self.controller.show_frame(CodeDisplayPage)

    
class CodeDisplayPage(ttk.Frame):
    """Container for the frame that contains reviewed code.
    
    In this frame the user will have their code that has been reviewed displayed to them. 
    they have the option to save the code at the top of the program with the comments in it. 
    
    Args:
        ttk (Frame): Frame widget that contains other widgets using ttk for stylization.
    """
    def __init__(self, parent, controller):
        """__init__ Initializes the container and its widgets."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.code_Display = tk.Text(self, wrap=tk.NONE, 
                width=60, height=20, font=("Consolas", 12))
        self.text_Population
        
    def text_Population(self):
        """Frame building function for the CodeDisplayPage
        
        Calling this function will build the frame and then populate the text box
        with the users code with the comments from ChatGPT. If this function is called
        without having comments from ChatGPT it will not populate the page. 
        
        """
        self.clear_page
        
        #Populates the page ONLY if ChatGPT has outputted. 
        if len(self.controller.chatgpt_comments) > 0: 
            
            code_list = self.controller.code.splitlines()
            error_line_numbers = []
            code_with_comments = []
            line_Number = 0
            error_index = 0
            
            ttk.Label(self, text="Here Is your code!", 
            font=("Times New Roman", 18), background="#121841",
            foreground="#C93D4F").grid(column=0, row=0, padx=2, pady=2)
            
            self.code_Display = tk.Text(self, wrap=tk.NONE, 
                width=60, height=20, font=("Consolas", 12))
            
            self.code_Display.grid(column=0, row=1, pady=2,
                padx=2, sticky="nsew")
            
            scrollY = ttk.Scrollbar(self, command=self.code_Display.yview)
            scrollY.grid(row=1, column=1, sticky='nsew')
            self.code_Display['yscrollcommand'] = scrollY.set
            
            scrollX = ttk.Scrollbar(self, orient="horizontal" ,
                command=self.code_Display.xview)
            scrollX.grid(row=2, column=0, sticky='nsew')
            self.code_Display['xscrollcommand'] = scrollX.set
            
            #For each pylint comment it appends error numbers
            #to the list in the order given by Pylint
            for i in self.controller.pylint_comments:
                digit = 0 
                number = ""
                for j in range(len(i)):
                    if i[j].isdigit():
                        number += i[j]
                        digit += 1
                    elif i[j] == ':':
                        error_line_numbers.append(number)
                        break
                    
            #for each code output it checks if the current line 
            #being appended to the code with comments list has a 
            #error associated with it. If it does it appends the code
            #after the line it is for.        
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
        """Styles the container and widgets."""
        self.code_Display.config(undo=True, background="#262335", 
            borderwidth=3, relief="sunken", foreground="#F573C8")
        
        style=ttk.Style()
        style.theme_use('classic')
        style.configure("Vertical.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
        style.configure("Horizontal.TScrollbar",
            background="#A65D34", troughcolor = "#241B2F")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.grid_propagate(False)
            
        self.config(bg='#121841')   
        
    def save(self):
        """save, saves the text that is currently in code_Display.
        
        When called, the program will open up a file dialog for the user. 
        When the user chooses where to save the txt file the program will pull from the 
        code_Display text box and save it.  
        
        """
        if len(self.code_Display.get('1.0', 'end-1c')) > 0:
            f = asksaveasfile(initialfile = 'CommentedCode.txt',
                defaultextension=".txt", filetypes=[("All Files","*.*")])
            code = self.code_Display.get('1.0', 'end-1c')
            f.write(code)
            f.close
    
    def update_size(self, event):
        """Resizes widgets in window when window is resized."""
        width = event.width
        height = event.height
        self.code_Display.config(width=width // 10, height=height // 30) 
          
    def clear_page(self):
        """clear_page Deletes all widgets in current container."""
        for widget in self.winfo_children():
            widget.destroy()
 
class ChatGptThreaded(threading.Thread): 
    def __init__(self, queue, comments, code):
        super().__init__()
        self.queue = queue
        self.comments = comments
        self.code = code
        
    def run(self):
        """
        Takes Pylint output and sends it to ChatGPT to reword comments for new users. 
        ChatGPT is sent a priming message and the code for review along with individual 
        outputs from Pylint. This happens for each output from Pylint. Then sets chatgpt_comments equal 
        to the comments made by ChatGPT
        """
        comment_list = []
        
        #Creating a priming message as the system to tell ChatGPT how to respond
        #To the user 
        messages = [ {"role": "system", "content": """
        Hello ChatGPT,

        I am working on a Python program aimed at helping new computer scientists understand their code better. 
        The program takes input code from users who are new to Python and runs pylint on it to identify issues.
        However, the output from pylint can be difficult for beginners to grasp due to its technical language and jargon.

        I need your assistance in making the pylint outputs more readable and user-friendly. 
        The goal is to generate clear and concise comments that explain the issues detected by pylint in a simple and easy-to-understand manner. 
        Imagine you are explaining these concepts to someone who is just starting to learn Python programming.
        I will give you the whole program from the student and individual errors codes for you to reword.
    
        Example pylint output for interpretation:
        :1:0: C0116: Missing function or method docstring (missing-function-docstring)
        1. The :1: is the line where pylint says the error is.
        2. The Second number in-between colons in this example :0: doesn't mean anything in any case you will look at.
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

        messages.append(
            {"role": "system", "content": ("here is the users code: " + self.code)}
        )
        
        total_comments = len(self.comments)
        progress = 0
        amount_processed = 0
        
        #Sends ChatGPT a priming message, the user code, and pylint code 
        #For each code generated by Pylint. 
        for i in self.comments:
            if len(messages) > 2:
                messages.pop()
                print(i)
                messages.append(
                    {"role": "user", "content": i}    
                )
            else:
                messages.append(
                    {"role": "user", "content": i}    
                )
                print(i)
        
            chat = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo", messages=messages 
            )
            
            reply = chat.choices[0].message.content 
            
            comment_list.append(reply)
            
            progress = int((len(comment_list) / total_comments) * 100)
            self.queue.put(progress)
            print("Progress!")
        
        self.queue.put({"progress": 100, "result": comment_list})
        
if __name__ == "__main__": 

    
    api_key_file = open("C:/Users/larry/OneDrive/Desktop/API KEY.txt", 'r')
    openai.api_key = api_key_file.read()
    
    testObj = windows()
    testObj.geometry("800x600")
    testObj.mainloop()