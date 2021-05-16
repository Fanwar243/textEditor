import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import font as tkFont

class Scribble:

    def __init__(self, root):
        self.root = root
        self.root.title("Untitled note")
        self.root.geometry("1280x720")
        self.root.minsize(400, 200)
        self.root.title("Scribbler - Untitled")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.filename = None
        self.saved = False

        #scrollbar
        scroll = tk.Scrollbar(self.root, orient = "vertical")
        scroll.pack(side = "right", fill = "y")

        #text area
        self.txtarea = tk.Text(self.root, yscrollcommand = scroll.set, undo = True)
        self.txtarea.pack(fill = "both", expand = "1")

        #top menu bar
        self.menubar = tk.Menu(self.root, bg = "#808080")
        self.root.config(menu = self.menubar)

        fileMenu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "Open", accelerator = "Ctrl+O", command = self.openfile)
        fileMenu.add_command(label = "New File", accelerator = "Ctrl+N", command = self.newfile)
        fileMenu.add_command(label = "Save", accelerator = "Ctrl+S", command = self.savefile)
        fileMenu.add_command(label = "Save As...", accelerator = "Ctrl+Shift+S", command = self.saveas)
        fileMenu.add_command(label = "Quit", accelerator = "Ctrl+W", command = self.exit)

        editMenu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Edit", menu = editMenu)
        editMenu.add_command(label = "Copy", accelerator = "Ctrl+C", command = self.txtarea.event_generate("<<Copy>>"))
        editMenu.add_command(label = "Cut", accelerator = "Ctrl+X", command = self.txtarea.event_generate("<<Cut>>"))
        editMenu.add_command(label = "Paste", accelerator = "Ctrl+V", command = self.txtarea.event_generate("<<Paste>>"))
        editMenu.add_command(label = "Undo", accelerator = "Ctrl+Z", command = self.txtarea.edit_undo)
        editMenu.add_command(label = "Redo", accelerator = "Ctrl+Y", command = self.txtarea.edit_redo)

        textMenu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "Format", menu = textMenu)
        textMenu.add_command(label = "Bold", accelerator = "Ctrl+B", command = self.toggle_bold)
        textMenu.add_command(label = "Italics", accelerator = "Ctrl+I", command = self.toggle_italics)
        textMenu.add_command(label = "Underline", accelerator = "Ctrl+U", command = self.toggle_underline)
        textMenu.add_command(label = "Align center", accelerator = "Ctrl+J", command = self.justify_center)

        aboutMenu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "About", menu = aboutMenu)
        aboutMenu.add_cascade(label = "About this program", command = self.popup)

        #keyboard shortcuts
        self.txtarea.bind("<Control-o>", self.openfile)
        self.txtarea.bind("<Control-n>", self.newfile)
        self.txtarea.bind("<Control-s>", self.savefile)
        self.txtarea.bind("<Control-S>", self.saveas)
        self.txtarea.bind("<Control-c>", self.txtarea.event_generate("<<Copy>>"))
        self.txtarea.bind("<Control-x>", self.txtarea.event_generate("<<Cut>>"))
        self.txtarea.bind("<Control-v>", self.txtarea.event_generate("<<Paste>>"))
        self.txtarea.bind("<Control-z>", self.txtarea.edit_undo)
        self.txtarea.bind("<Control-y>", self.txtarea.edit_redo)
        self.txtarea.bind("<Control-b>", self.toggle_bold)
        self.txtarea.bind("<Control-i>", self.toggle_italics)
        self.txtarea.bind("<Control-u>", self.toggle_underline)
        self.txtarea.bind("<Control-g>", self.toggle_strikeout)
        self.txtarea.bind("<Control-j>", self.justify_center)
        self.txtarea.bind("<Control-w>", self.exit)

    #if modified, saved = false

    def exit(self, *args):
        if self.saved == False:
            confirm = messagebox.askokcancel(title = "Warning", message = "Changes unsaved. Exit anyway?")
            if confirm:
                self.root.destroy()
        else:
            self.root.destroy()
    
    def savefile(self, *args):
        if self.filename == None:
            files = [('All Files', '*.*'), ('Text Document', '*.txt')]
            self.filename =  fd.asksaveasfilename(initialdir = "/", title = "Select file", filetypes = files)
        if self.filename == '':
            self.filename = None
        if self.filename != None and self.filename != '':
            content = self.txtarea.get("1.0", "end")
            file = open(self.filename, "w")
            file.write(content)
            file.close()
            self.saved = True
            self.root.title("Scribbler - " + file.name)
            messagebox.showinfo(title = "Info", message = "File saved successfully.")

    def openfile(self, *args):
        self.filename = fd.askopenfilename(initialdir = "/", title = "Select file", filetypes = [('All Files', '*.*'), ('Text Document', '*.txt')])
        file = open(self.filename)
        if file is not None:
            self.txtarea.delete("1.0", "end")
            content = file.read()
            self.root.title("Scribbler - " + file.name)
            self.txtarea.insert("1.0", content)
    
    def newfile(self, *args):
        if self.saved == False:
            confirm = messagebox.askokcancel(title = "Warning", message = "Changes unsaved. Continue?")
            if confirm:
                self.txtarea.delete("1.0", "end")
                self.root.title("Scribbler - Untitled")
                self.filename = None
        else:
            self.txtarea.delete("1.0", "end")
            self.root.title("Scribbler - Untitled")
            self.filename = None


    def saveas(self, *args):
        files = [('All Files', '*.*'), ('Text Document', '*.txt')]
        self.filename =  fd.asksaveasfilename(initialdir = "/", title = "Select file", filetypes = files)
        content = self.txtarea.get("1.0", "end")
        file = open(self.filename, "w")
        file.write(content)
        file.close()
        self.saved = True
        messagebox.showinfo(title = "Info", message = "File saved successfully.")

    def toggle_bold(self, *args):
        boldFont = tkFont.Font(weight = "bold")
        self.txtarea.tag_configure("boldtext", font = boldFont)
        if "boldtext" in self.txtarea.tag_names("sel.first"):
            self.txtarea.tag_remove("boldtext", "sel.first", "sel.last")
        else:
            self.txtarea.tag_add("boldtext", "sel.first", "sel.last")

    def toggle_italics(self, *args):                                                    #STILL DOESN'T WORK
        myFont = tkFont.Font(slant = "italic")
        self.txtarea.tag_configure("italtext", font = myFont)
        if "italtext" in self.txtarea.tag_names("sel.first"):
            self.txtarea.tag_remove("italtext", "sel.first", "sel.last")
        else:
            self.txtarea.tag_add("italtext", "sel.first", "sel.last")

    def toggle_underline(self, *args):
        self.txtarea.tag_configure("underline", underline = True)
        if "underline" in self.txtarea.tag_names("sel.first"):
            self.txtarea.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.txtarea.tag_add("underline", "sel.first", "sel.last")

    def toggle_strikeout(self, *args):
        self.txtarea.tag_configure("strikeout", overstrike = True)
        if "strikeout" in self.txtarea.tag_names("sel.first"):
            self.txtarea.tag_remove("strikeout", "sel.first", "sel.last")
        else:
            self.txtarea.tag_add("strikeout", "sel.first", "sel.last")

    def justify_center(self, *args):
        self.txtarea.tag_configure("center", justify = "center")
        if "center" in self.txtarea.tag_names("sel.first"):
            self.txtarea.tag_remove("center", "sel.first", "sel.last")
        else:
            self.txtarea.tag_add("center", "sel.first", "sel.last")

    def popup(self, *args):
        popup = messagebox.showinfo(title = "About", message = "A GUI application project started by Fanwar243 in May 2021.")

    
if __name__ == "__main__":
    root = tk.Tk()
    Scribble(root)
    root.mainloop()