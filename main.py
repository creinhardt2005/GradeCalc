from tkinter import Tk
from gui import GradeCalc

def main():
    root = Tk()
    app = GradeCalc(root)
    root.geometry('550x375')
    root.mainloop()

if __name__ == "__main__":
    main()
