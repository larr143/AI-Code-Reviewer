import tkinter as tk 
from tkinter import ttk 
from tkinter import scrolledtext
import os 


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
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
        

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self,parent)
        
        ttk.Label(self, text="Welcome! Please input your code below, then click the next button!", 
          font=("Times New Roman", 15)).grid(column=0, row=0, expand=True) 
        
        entry = scrolledtext.ScrolledText(self)
        
        vbar = tk.Scrollbar(self, orient="vertical", command=entry.yview)
        hbar = tk.Scrollbar(self, orient="horizontal", command=entry.xview)
        
        # vbar.pack(side="right", fill="y")
        # hbar.pack(side="bottom", fill="x")
        vbar.grid(column=1, row=0, expand=True)
        hbar.grid(column=0,row=2, expand=True)
        
        entry.grid(column=0,row=1, expand=True)
        
        # text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, 
        #     width=60, height=18, font=("Times New Roman", 15)) 
  
        # text_area.grid(column=0, row=1, pady=10, padx=10)


    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
     
     
     
class LoadingPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="This Is the Search Page")
        label.pack(padx=10, pady=10)
        
        next_Button = tk.Button(
            self,
            text = "Next Page",
            command=lambda: controller.show_frame(CodeDisplayPage)
        )
        next_Button.pack(side="bottom", fill=tk.X)
        
        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(MainPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        
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

    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
        

        
            
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()