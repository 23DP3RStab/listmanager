import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import json

class ShoppingListManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        #--- Main Window ---#
        self.title("Shopping List Manager")
        self.resizable(False, False)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self._set_appearance_mode("system")
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
        self.listframe = ctk.CTkScrollableFrame(self, width=500, height=425)
        self.listframe.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="nw")
        self.listframe.grid_columnconfigure(0, weight=1)

        self.createlist = ctk.CTkButton(self, text="Create List", command=self.addList, width=520)
        self.createlist.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="sw")

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
        pass

    def editList(self):
        pass

    def loadLists(self):
        if not os.path.exists("lists"):
            os.makedirs("lists")
        
        self.listcount = len(os.listdir("lists"))
        self.listframe.grid_rowconfigure(self.listcount, weight=1)

        for i in range(self.listcount):
            self.listname = os.listdir("lists")[i]
            self.listname = self.listname[:-5]

            self.listbutton = ctk.CTkButton(self.listframe, text=self.listname, command=lambda: self.openList(self.listname))
            self.listbutton.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")
            



if __name__ == "__main__":
    app = ShoppingListManager()
    app.loadLists()
    app.mainloop()
