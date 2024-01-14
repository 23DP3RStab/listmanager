import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import json
import tkinter as tk

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

        self.center(self, 1000, 500)

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
        self.addwindow.title("Add")
        self.addwindow.resizable(False, False)
        self.addwindow.grid_rowconfigure(0, weight=1)
        self.addwindow.grid_columnconfigure(0, weight=1)

        self.addwindow.attributes('-topmost', True)
        self.addwindow.focus_force()

        self.center(self.addwindow, 200, 100)

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

        #--- Add List extra ---#
        self.addwindow.after(1, lambda: self.listnameentry.focus_set())


    def savelist(self):
        self.listname = self.listnameentry.get()
        
        if not os.path.exists("lists"):
            os.makedirs("lists")

        with open(f'lists/{self.listname}.json', 'w') as f:
            json.dump([], f)


    def deleteList(self):
        if self.selectedlistname is None:
            self.popupmsg("No list selected!")
            return

        if self.selectedlistname in self.listbuttons:
            buttondelete = self.listbuttons[self.selectedlistname]

            buttondelete.destroy()

            del self.listbuttons[self.selectedlistname]

        list_file_path = f"lists/{self.selectedlistname}.json"
        if os.path.exists(list_file_path):
            os.remove(list_file_path)
            self.popupmsg("List deleted!")

        self.selectedlist = None
        self.selectedlistname = None


    def editList(self):
        if self.selectedlist is None:
            self.popupmsg("No list selected!")
            return
        
        self.editwindow = ctk.CTkToplevel(self)
        self.editwindow.title("Edit")
        self.editwindow.resizable(False, False)

        self.editwindow.attributes('-topmost', True)
        self.editwindow.focus_force()

        self.center(self.editwindow, 200, 325)

        #--- Edit List Widgets ---#
        self.editlistframe = ctk.CTkFrame(self.editwindow)
        self.editlistframe.pack(padx=5, pady=5, anchor="center", fill="both", expand=True)

        self.itemname = ctk.CTkLabel(self.editlistframe, text="Item Name:", anchor="w")
        self.itemname.pack(padx=10, pady=(10, 0))

        self.itemnameentry = ctk.CTkEntry(self.editlistframe, width=175)
        self.itemnameentry.pack(padx=10, pady=(0, 10))

        self.itemprice = ctk.CTkLabel(self.editlistframe, text="Item Price:", anchor="w")
        self.itemprice.pack(padx=10, pady=(10, 0))

        self.itempriceentry = ctk.CTkEntry(self.editlistframe, width=175)
        self.itempriceentry.pack(padx=10, pady=(0, 10))

        self.itemquantity = ctk.CTkLabel(self.editlistframe, text="Item Quantity:", anchor="w")
        self.itemquantity.pack(padx=10, pady=(10, 0))

        self.itemquantityentry = ctk.CTkEntry(self.editlistframe, width=175)
        self.itemquantityentry.pack(padx=10, pady=(0, 10))

        def saveItem():
            item_name = self.itemnameentry.get()
            item_price = self.itempriceentry.get()
            item_quantity = self.itemquantityentry.get()

            with open(f"lists/{self.selectedlistname}.json", "r+") as file:
                list_data = json.load(file)

                list_data.append({
                    "name": item_name,
                    "price": item_price,
                    "quantity": item_quantity
                })

                file.seek(0)
                file.truncate()
                json.dump(list_data, file)
            
            self.itemnameentry.delete(0, "end")
            self.itempriceentry.delete(0, "end")
            self.itemquantityentry.delete(0, "end")

            self.popupmsg("Item added!")

        self.additembutton = ctk.CTkButton(self.editlistframe, text="Add Item", command=saveItem)
        self.additembutton.pack(padx=10, pady=10)

        self.exitbutton = ctk.CTkButton(self.editlistframe, text="Done", command=self.editwindow.destroy)
        self.exitbutton.pack(padx=10, pady=(0, 10))

        self.editwindow.bind("<Return>", lambda event: saveItem())


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
        try:
            if self.selectedlist is not None:
                self.selectedlist.configure(fg_color="#2b2b2b", border_color="#1f6aa5")
        except AttributeError:
            self.popupmsg("An error occurred!")

        self.selectedlist = self.listbuttons[listname]
        self.selectedlistname = listname

        self.selectedlist.configure(fg_color="#1f6aa5", border_color="#1f6aa5")

        self.displayList()
    

    def popupmsg(self, msg):
        if hasattr(self, 'editwindow') and self.editwindow is not None:
            self.editwindow.attributes('-topmost', False)

        popup = ctk.CTkToplevel()
        popup.title("!")
        popup.resizable(False, False)
        popup.attributes('-topmost', 1)
        popup.focus_force()

        self.center(popup, 200, 100)

        label = ctk.CTkLabel(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)

        B1 = ctk.CTkButton(popup, text="Okay", command=lambda: [popup.destroy(), self.editwindow.attributes('-topmost', True) if hasattr(self, 'editwindow') and self.editwindow is not None else None])
        B1.pack()


    def center(self, toplevel, w, h):
        ws = toplevel.winfo_screenwidth()
        hs = toplevel.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def displayList(self):
        with open(f"lists/{self.selectedlistname}.json", "r") as file:
            list_data = json.load(file)

        if len(list_data) == 0:
            self.popupmsg("List is empty!")
            return

        fig, ax = plt.subplots()

        ax.axis('off')

        table_data = []
        for item in list_data:
            row = [item['name'], item['price'], item['quantity']]
            table_data.append(row)

        table = ax.table(cellText=table_data, colLabels=["Item Name", "Price", "Quantity"], cellLoc = 'center', loc='center')

        plt.show()



if __name__ == "__main__":
    app = ShoppingListManager()
    app.loadLists()
    app.mainloop()
