import tkinter as tk 
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
        for F in (MainPage, SearchPage):
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
        label = tk.Label(self, text="Welcome")
        label.pack(padx=10,pady=10)


    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()
     
     
     
class SearchPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="This Is the Search Page")
        label.pack(padx=10, pady=10)

        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(MainPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        

        
            
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()