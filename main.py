import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os

class ShoppingListManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        #--- Main Window ---#
        self.title("Shopping List Manager")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self._set_appearance_mode("system")
        self.bind("<End>", lambda event: self.destroy())

        #--- Window Size ---#
        self.w = 1500
        self.h = 750

        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()

        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)

        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        #--- Window Widgets ---#
        self.buttonframe = ctk.CTkFrame(self)
        self.buttonframe.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="nsw")

        self.listframe = ctk.CTkFrame(self)
        self.listframe.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.addlist = ctk.CTkButton(self.buttonframe, text="Add List", command=self.addList)
        self.addlist.pack(padx=10, pady=10)

        self.dellist = ctk.CTkButton(self.buttonframe, text="Delete List", command=self.deleteList)
        self.dellist.pack(padx=10, pady=10)

        self.editlist = ctk.CTkButton(self.buttonframe, text="Edit List", command=self.editList)
        self.editlist.pack(padx=10, pady=10)

        self.exitbutton = ctk.CTkButton(self.buttonframe, text="Exit", command=self.destroy)
        self.exitbutton.pack(padx=10, pady=10, side="bottom")

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
        h = 200

        ws = self.addwindow.winfo_screenwidth()
        hs = self.addwindow.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.addwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

        #--- Add List Widgets ---#
        self.addlistframe = ctk.CTkFrame(self.addwindow)
        self.addlistframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.listname = ctk.CTkLabel(self.addlistframe, text="List Name:")
        self.listname.pack(padx=10, pady=10)

        self.listnameentry = ctk.CTkEntry(self.addlistframe)
        self.listnameentry.pack(padx=10)

        self.addlistbutton = ctk.CTkButton(self.addlistframe, text="Add List", command=lambda: [self.savelist(), self.addwindow.destroy()])
        self.addlistbutton.pack(padx=10, pady=10)

         



        #--- Add List mainloop ---#
        self.addwindow.mainloop()

    def savelist(self):
        self.listname = self.listnameentry.get()
        os.mkdir("lists/" + self.listname)

    def deleteList(self):
        pass

    def editList(self):
        pass

if __name__ == "__main__":
    app = ShoppingListManager()
    app.mainloop()
