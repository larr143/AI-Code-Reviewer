import tkinter as tk 
from tkinter import ttk 
from tkinter import scrolledtext
import os 
import ast
import openai
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import tempfile
    

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Adding a title to the window
        self.wm_title("Code Reviewer")

        # creating a frame and assigning it to container
        container = tk.Frame(self, width=400,height=600)
        
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        
        
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, LoadingPage, CodeDisplayPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Using a method to switch frames
        self.show_frame(MainPage)
        
        # Creating a bind for when the size ofthe frame changes then sending the update size command to the frame.
        self.bind("<Configure>", self.frames[MainPage].update_size)
        self.prev_width = self.winfo_width()
        self.prev_height = self.winfo_height()
        
        #creating the variables that store code and the comments. 
        self.code = ""
        self.pylint_comments = ""
        self.chatgpt_comments = ""           

        
    def pylint_Processing(self):
        
        code = self.code
        
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
        Run([temp_file_path, "--rcfile", custom_rcfile], reporter=reporter, exit=False)

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
            modified_output[i] = modified_output[i].lstrip(temp_file_path)
            
        self.pylint_comments = modified_output
        
        self.show_frame(LoadingPage)
        
        
        
        
    def show_frame(self, cont):
        frame = self.frames[cont]
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
            
            

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.isvalid = None
        self.what_to_display()
        
    def what_to_display(self):
        
        self.clear_page()
        
        ttk.Label(self, text="Welcome! Please input your code below, then click the next button!", 
          font=("Times New Roman", 15)).grid(column=0,row=0,padx=10,pady=10)
        
               
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.NONE, 
            width=60, height=18, font=("Times New Roman", 15)) 
  
        self.text_area.grid(column=0, row=1, pady=10, padx=10, sticky="nsew")
        
        # Create a horizontal scrollbar
        horizontal_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text_area.xview)
        horizontal_scrollbar.grid(column=0, row=2, sticky='ew', padx=10)
        
        # Configure the horizontal scrollbar to work with the text widget
        self.text_area.config(xscrollcommand=horizontal_scrollbar.set)
        
        print(self.isvalid)
        
        if type(self.isvalid) == bool:
            if not self.isvalid:
                validtext = tk.Label(self, text="your code is not valid, please try again!")
                validtext.grid(column=0, row=4, pady=10, padx=10, sticky="nsew")
            else: 
                validtext = tk.Label(self, text="")
                validtext.grid(column=0, row=4, pady=10, padx=10, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1) 
        
        self.button = tk.Button(
            self,
            text="Next",
            command=lambda: self.code_Checker()
        )
        self.button.grid(column=0, row=3, pady=10, padx=1)  
        
    
    def code_Checker(self):
        try:
            ast.parse(self.text_area.get('1.0', 'end-1c'))
            print("parsed")
            self.isvalid = True
        except SyntaxError:
            print('False')
            self.isvalid = False
            self.what_to_display()
        
        
        if self.isvalid == True:
            print("")
            self.isvalid = True
            self.controller.code = self.text_area.get("1.0", "end-1c")
            self.controller.pylint_Processing()

        
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
     
     
     
class LoadingPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.what_to_display()
        
        
    def what_to_display(self):
        
        self.clear_page()
        
        label = tk.Label(self, text="Loading Code...")
        label.pack(padx=10, pady=10) 
        
        
        
        
    def chatgpt_Proccessing():
        pass
        
        
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
        
        
class CodeDisplayPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="This Is the Code Display Page")
        label.pack(padx=10, pady=10)

        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(LoadingPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)

    def update_size(self, width, height):
        pass

    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
        

        
            
if __name__ == "__main__":
    testObj = windows()
    #Set initial size 
    testObj.geometry("800x600")
    testObj.mainloop()