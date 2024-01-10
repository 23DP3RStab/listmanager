import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import json

class ShoppingListManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.selectedlist = None
        self.selectedlistname = None

        #--- Main Window ---#
        self.title("Shopping List Manager")
        self.resizable(False, False)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self._set_appearance_mode("dark")
        self.bind("<End>", lambda event: self.destroy())

        #--- Window Size ---#
        self.w = 1000
        self.h = 500

        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()

        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)

        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        #--- Window Widgets ---#
        self.listframe = ctk.CTkScrollableFrame(self, width=365, height=425)
        self.listframe.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="nw")
        self.listframe.grid_columnconfigure(0, weight=1)

        self.refreshbutton = ctk.CTkButton(self, text="Refresh", command=self.loadLists, width=185)
        self.refreshbutton.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="sw")

        self.createlist = ctk.CTkButton(self, text="Create List", command=self.addList, width=190)
        self.createlist.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="se")

        self.deletebutton = ctk.CTkButton(self, text="Delete List", command=lambda:self.deleteList(), width=190)
        self.deletebutton.grid(row=1, column=3, padx=(0, 10), pady=(0, 10), sticky="sw")

        self.editbutton = ctk.CTkButton(self, text="Edit List", command=self.editList, width=190)
        self.editbutton.grid(row=1, column=4, padx=(0, 10), pady=(0, 10), sticky="se")

        self.settingsbutton = ctk.CTkButton(self, text="Settings", width=190)
        self.settingsbutton.grid(row=1, column=5, padx=(0, 10), pady=(0, 10), sticky="sw")



    def addList(self):

        #--- Add List Window ---#
        self.addwindow = ctk.CTkToplevel(self)
        self.addwindow.title("Add List")
        self.addwindow.resizable(False, False)
        self.addwindow.grid_rowconfigure(0, weight=1)
        self.addwindow.grid_columnconfigure(0, weight=1)

        self.addwindow.attributes('-topmost', 1)
        self.addwindow.focus_force()

        w = 200
        h = 100

        ws = self.addwindow.winfo_screenwidth()
        hs = self.addwindow.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.addwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

        #--- Add List Widgets ---#
        self.addlistframe = ctk.CTkFrame(self.addwindow)
        self.addlistframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.listname = ctk.CTkLabel(self.addlistframe, text="List Name:")
        self.listname.pack(padx=10, pady=(10, 5))

        self.listnameentry = ctk.CTkEntry(self.addlistframe)
        self.listnameentry.pack(padx=10, pady=(5, 10))
        self.listnameentry.bind("<Return>", lambda event: [self.savelist(), self.addwindow.destroy()])

        self.addlistbutton = ctk.CTkButton(self.addlistframe, text="Add List", command=lambda: [self.savelist(), self.addwindow.destroy()])
        self.addlistbutton.pack(padx=10, pady=10)

        #--- Add List mainloop ---#
        self.addwindow.mainloop()


    def savelist(self):
        self.listname = self.listnameentry.get()
        
        if not os.path.exists("lists"):
            os.makedirs("lists")

        with open(f'lists/{self.listname}.json', 'w') as f:
            json.dump("random", f)


    def deleteList(self):
        if self.selectedlistname is None:
            self.popupmsg("No list selected!")
            return
        self.listbuttons.pop(self.selectedlistname)
        os.remove(f"lists/{self.selectedlistname}.json")
        self.popupmsg("List deleted!")


    def editList(self):
        if self.selectedlist is None:
            self.popupmsg("No list selected!")
            return
        self.editwindow = ctk.CTkToplevel(self)


    def loadLists(self):
        if not os.path.exists("lists"):
            os.makedirs("lists")

        self.listcount = len(os.listdir("lists"))
        self.listframe.grid_rowconfigure(self.listcount, weight=1)

        self.listbuttons = {}

        def make_command(name):
            return lambda: self.selectList(name)

        for i in range(self.listcount):
            self.listname = os.listdir("lists")[i]
            self.listname = self.listname[:-5]

            self.listbuttons[self.listname] = ctk.CTkButton(self.listframe, text=self.listname, command=make_command(self.listname), hover=True, fg_color="#2b2b2b", border_color="#1f6aa5", border_width=1)
            self.listbuttons[self.listname].grid(row=i, column=0, padx=10, pady=(5, 0), sticky="nsew")


    def selectList(self, listname):
        if self.selectedlist is not None:
            self.selectedlist.configure(fg_color="#2b2b2b", border_color="#1f6aa5")

        self.selectedlist = self.listbuttons[listname]
        self.selectedlistname = listname
        print(self.selectedlist)
        print(self.selectedlist.cget("text"))
        print(self.selectedlistname)

        self.selectedlist.configure(fg_color="#1f6aa5", border_color="#1f6aa5")
    
    def popupmsg(self, msg):
        popup = ctk.CTkToplevel()
        popup.title("!")
        popup.resizable(False, False)
        popup.attributes('-topmost', 1)
        popup.focus_force()
        popup.geometry("200x100")

        label = ctk.CTkLabel(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)

        B1 = ctk.CTkButton(popup, text="Okay", command = popup.destroy)
        B1.pack()

        popup.mainloop()



if __name__ == "__main__":
    app = ShoppingListManager()
    app.loadLists()
    app.mainloop()
