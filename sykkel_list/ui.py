from tkinter import *
from .osmgr import FIELD_NAME, FIELD_NUM_BIKES_AVAILABLE, FIELD_NUM_DOCKS_AVAILABLE

class WindowSykkelList():
    def __init__(self, stations_list):
        self.root = Tk()
        self.root.geometry("400x800")

        self.label_title = Label(self.root, text="Oslo Sykkel Availability", font="26")
        self.label_title.pack()

        self.scroll = Scrollbar(self.root)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.set_sykkel_data(stations_list)

    def set_sykkel_data(self, stations_list):
        # 
        self.list_box = Listbox(self.root, yscrollcommand=self.scroll.set, height=0)
        for station in stations_list.values():
            text = "{}:  {} bikes / {} docks".format(station.get(FIELD_NAME, "ERROR_NAME_NOTFOUND"),
                                                      station.get(FIELD_NUM_BIKES_AVAILABLE, "ERROR_DATA_NOTFOUND"),
                                                      station.get(FIELD_NUM_DOCKS_AVAILABLE, "ERROR_DATA_NOTFOUND"))
            self.list_box.insert(END, text)
        self.list_box.pack(fill=BOTH)
        
        

    def show(self):
        self.root.mainloop()


