import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import pm 

root = Tk()
window_width = 1280
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.minsize(1150, 500)
root.title("Password Manager by Stevees")

root.title("Password Manager by Stevees")
# icon = PhotoImage(file = 'bill_icon.png')
# root.iconphoto(True,icon)

#namelabel Top
nameLabel = Frame(root, relief='ridge', borderwidth=1, bg='gray80')
namePlaceHolder = Label(nameLabel, text='Password Manager') #font text or image can be changed
namePlaceHolder.pack(pady=10)
nameLabel.pack(fill=X)

#Global Variables
masterPass_Input_Var, masterPass_ReEnter_Input_Var, service_Input_Var, password_Input_Var, email_Input_Var, note_Input_Var = [None]*6

# Button Functions

def defaultDisplay_Hide():

    # defaultDisplay.destroy()    
    # defaultDisplay.place_forget()
    # defaultDisplay.pack_forget()    
    # defaultDisplay.grid_forget()

    global displayFrame
    displayFrame.pack_forget()
    # displayFrame.destroy()
    displayFrame = LabelFrame(frame1, text='DisplayFrame', relief=FLAT, bd=3)
    displayFrame.pack(expand=True, fill=BOTH, padx=5, pady=5)

    pass



def helpDisplay():  # Button 8

    defaultDisplay_Hide()       

    defaultDisplay = Label(displayFrame,bg='silver', text=helpText,bd=4,font="helvatica", wraplength=900, padx=10, pady=10)
    defaultDisplay.pack(expand=True, fill=BOTH, padx=5, pady=5)
    # defaultDisplay.place(anchor=CENTER, relx=0.5, rely=0.3)

    pass  

def showDefaultDisplay():
    defaultDisplay_Hide()  # Nascondi il frame attuale
    defaultDisplay = Label(displayFrame, bg='silver', text=
    "Password Manager by Stevees.\n\nPress any button from above to being OR 'Help' for full list of Info\n\n'WARNING: You must use the same MASTER PASSWORD for both adding and retrieving a password, otherwise the service cannot be provided!'",
    bd=4, font="helvetica", wraplength=900, padx=10, pady=10)
    defaultDisplay.place(anchor=CENTER, relx=0.5, rely=0.3)

def addCreds(): # Button 1

    defaultDisplay_Hide()        

    global masterPass_Input_Var, masterPass_ReEnter_Input_Var, service_Input_Var, password_Input_Var, email_Input_Var, note_Input_Var, credsSubmit

    masterPass_Input_Var = StringVar()
    masterPass_ReEnter_Input_Var = StringVar()
    service_Input_Var = StringVar()
    password_Input_Var = StringVar()
    email_Input_Var = StringVar()
    note_Input_Var = StringVar() # optional

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.3, rely=0.2, anchor=CENTER, x=-50)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show="*")
    masterPass_Input.place(relx=0.4, rely=0.2, anchor=CENTER)

    masterPass_ReEnter_Label = Label(displayFrame, text="Re-Enter MASTER PASSWORD :")
    masterPass_ReEnter_Label.place(relx=0.3, rely=0.3, anchor=CENTER, x=-58)
    masterPass_ReEnter_Input = Entry(displayFrame, width=30, textvariable=masterPass_ReEnter_Input_Var, show="*")
    masterPass_ReEnter_Input.place(relx=0.4, rely=0.3, anchor=CENTER)

    service_Label = Label(displayFrame, text="Service :")
    service_Label.place(relx=0.3, rely=0.4, anchor=CENTER, x=2)
    service_Input = Entry(displayFrame, width=30, textvariable=service_Input_Var)
    service_Input.place(relx=0.4, rely=0.4, anchor=CENTER)

    email_Label = Label(displayFrame, text="Email :")
    email_Label.place(relx=0.5, rely=0.2, anchor=CENTER, x=50)
    email_Input = Entry(displayFrame, width=30, textvariable=email_Input_Var)
    email_Input.place(relx=0.6, rely=0.2, anchor=CENTER, x=50)    

    password_Label = Label(displayFrame, text="Password :")
    password_Label.place(relx=0.5, rely=0.3, anchor=CENTER, x=41)
    password_Input = Entry(displayFrame, width=30, textvariable=password_Input_Var)
    password_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=50)

    note_Label = Label(displayFrame, text="Note :")
    note_Label.place(relx=0.5, rely=0.4, anchor=CENTER, x=52)
    optional_Label = Label(displayFrame, text="(Optional)")
    optional_Label.place(relx=0.8, rely=0.4, anchor=CENTER, x=-70)
    note_Input = Entry(displayFrame, width=30, textvariable=note_Input_Var)
    note_Input.place(relx=0.6, rely=0.4, anchor=CENTER, x=50)

    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=credsSubmit_func) # -> credsSubmit_func()
    credsSubmit.place(relx=0.5, rely=0.5, anchor=CENTER)

    pass

def credsSubmit_func(): 
    service = service_Input_Var.get()
    email = email_Input_Var.get()
    password = password_Input_Var.get()
    note = note_Input_Var.get()
    master_password = masterPass_Input_Var.get()
    master_password_confirmation = masterPass_ReEnter_Input_Var.get()

    if master_password != master_password_confirmation:
        messagebox.showwarning("Failed", "MASTER Password Not Matching\nPlease Re-Verify")
        print("Not Equal Password")
        return
    
    # Calling the add_password function with the extracted values
    if 1 == pm.add_password(service, email, password, note, master_password):
        messagebox.showinfo("Success", "Password succesfully stored.")
        showDefaultDisplay()         
    else:
        messagebox.showinfo("Failed", f"Error: Unable to add password. An entry with service '{service}' and email '{email}' already exists.")
        return
    



def viewAll():  #5 View All Database

    defaultDisplay_Hide()        

    global masterPass_Input_Var, popResult, credsSubmit
    masterPass_Input_Var = StringVar()
    # popResult = masterPass_Input_Var.get()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    # credsSubmit = Button(displayFrame, text='Submit',height=2, width=25, command=printAll, state=DISABLED)
    credsSubmit = Button(displayFrame, text='Submit',height=2, width=25, command=printAll)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)        
    pass

#Function Disable Sbbmit Button if Entered value == ""
# def enableCreds():
#     if masterPass_Input_Var.get() == "":
#         credsSubmit.config(state=DISABLED)    
#     else:
#         credsSubmit.config(state=NORMAL)            


def printAll(**kwargs): #5

    resultWindow = Toplevel(root)
    resultWindow.geometry("750x300")
    resultWindow.title("All your passwords")

    window_width = 750
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    resultWindow.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # Creare un Frame con una Scrollbar
    frame = Frame(resultWindow)
    frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Titolo della finestra
    Label(scrollable_frame, text="Result", font=('Helvetica 17 bold'), anchor="center").pack(pady=10, fill=X, expand=True)

    # Ottenere la master password e chiamare la funzione print_all
    popResult = masterPass_Input_Var.get()
    result = pm.print_all(popResult)
    

    
    # Mostrare i risultati nella finestra, centrati orizzontalmente
    if len(result) != 0:
        for el in result:
            Label(scrollable_frame, text=f"Service: '{el[0]}', Email: '{el[1]}', Password: '{el[2]}', Note: {el[3]}").pack(pady=5, fill=X, expand=True)
    else:
        Label(scrollable_frame, text="No results found.").pack(pady=10, fill=X, expand=True)

    pass




def searchByEmail(): #6

    defaultDisplay_Hide()        

    global masterPass_Input_Var, email_Input_Var

    masterPass_Input_Var = StringVar()
    email_Input_Var = StringVar()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.2, anchor=CENTER, x=35)

    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.2, anchor=CENTER, x=-35)

    email_Label = Label(displayFrame, text="Email :")
    email_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)

    email_Input = Entry(displayFrame, width=30, textvariable=email_Input_Var)
    email_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    def credsSubmit_func():
        email = email_Input_Var.get()
        master_password = masterPass_Input_Var.get()

        result = pm.find_by_mail(email, master_password)

        resultWindow = Toplevel(root)
        resultWindow.geometry("750x300")
        resultWindow.title("Search Results")

        window_width = 750
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        resultWindow.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        frame = Frame(resultWindow)
        frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        scrollable_frame = Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        Label(scrollable_frame, text="Search Results", font=('Helvetica 17 bold'), anchor="center").pack(pady=10, fill=X)

        if result:
            for el in result:
                if el[2] == "---":
                    Label(scrollable_frame, text=f"Error in decrtpting for service '{el[0]}' and email '{el[1]}'.", anchor="center").pack(pady=5, fill=X)
                else:
                    Label(scrollable_frame, text=f"Service: '{el[0]}', Email: '{el[1]}', Password: '{el[2]}', Note: {el[3]}", anchor="center").pack(pady=5, fill=X)
        else:
            Label(scrollable_frame, text="No results found or incorrect master password.", anchor="center").pack(pady=10, fill=X)
        showDefaultDisplay()   

    # Bottone di submit che chiama credsSubmit_func
    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=credsSubmit_func)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)


def delDatabase():
    defaultDisplay_Hide()        

    global masterPass_Input_Var, popResult, credsSubmit
    masterPass_Input_Var = StringVar()
    # popResult = masterPass_Input_Var.get()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    def delAll():
        confirm = messagebox.askyesno("Confirm Delete", "ATTENTION! This operation can't be undone. All datas will be lost. Are you sure you want to delete the entire database?")
        if confirm:
            if pm.delete_all(masterPass_Input.get()) == 1:
                messagebox.showinfo("Success", "Database succesfully deleted.")
            else:
                messagebox.showinfo("Failed", f"Error: Unable to delete database. Try again.")
            showDefaultDisplay()
    credsSubmit = Button(displayFrame, text='Submit',height=2, width=25, command=delAll)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)        
    pass

def quit():
    sys.exit(0)


pm.create_db()

#menu icons / buttons
menuButtons = Frame(root, relief='groove', borderwidth=1, bg='gray70', height=80)

menuButton1 = Button(menuButtons, text='Add New Credentials', height=2, width=15, command=addCreds).place(relx=0.1, rely=0.5, anchor=CENTER)
menuButton2 = Button(menuButtons, text='Search a Password', height=2, width=15).place(relx=0.2, rely=0.5, anchor=CENTER)
menuButton3 = Button(menuButtons, text='Modify a Password', height=2, width=15).place(relx=0.3, rely=0.5, anchor=CENTER)
menuButton4 = Button(menuButtons, text='Delete a Password', height=2, width=15).place(relx=0.4, rely=0.5, anchor=CENTER)
menuButton5 = Button(menuButtons, text='View All Database', height=2, width=15, command=viewAll).place(relx=0.5, rely=0.5, anchor=CENTER)
menuButton6 = Button(menuButtons, text='Search by Email', height=2, width=15, command=searchByEmail).place(relx=0.6, rely=0.5, anchor=CENTER)
menuButton7 = Button(menuButtons, text='Delete All Database', height=2, width=15, command=delDatabase).place(relx=0.7, rely=0.5, anchor=CENTER)
menuButton8 = Button(menuButtons, text='Help', height=2, width=15, command=helpDisplay).place(relx=0.8, rely=0.5, anchor=CENTER)
menuButton9 = Button(menuButtons, text='Quit', height=2, width=15, command=quit).place(relx=0.9, rely=0.5, anchor=CENTER)

menuButtons.pack(fill=BOTH)

#mainFrame
frame1 = LabelFrame(root, text='Main Page', bg='silver', relief=SOLID, bd=3)
frame1.pack(expand=True, fill=BOTH, padx=5, pady=5)

#DisplayFrame
displayFrame = LabelFrame(frame1, text='', relief=FLAT, bd=3)
displayFrame.pack(expand=True, fill=BOTH, padx=5, pady=5)


helpText="Choose the desired service by selecting the corresponding buttons from above."'\n''\n'"WARNING: You must use the same MASTER PASSWORD for both adding and retrieving a password, otherwise the service cannot be provided!"'\n''\n'"You will need to remember the MASTER PASSWORD, as it cannot be stored in the database."'\n''\n'"In the email field, you can enter either the email address used for that account or a Username or UserID."'\n''\n'"You can modify the service, email, password, and/or notes for each entry. The operation OVERWRITES the old data."'\n''\n'"You can delete an entry by confirming the service, email, and password, losing the respective information PERMANENTLY."

defaultDisplay = Label(displayFrame, bg='silver', text=
"Password Manager by Stevees.\n\nPress any button from above to being OR 'Help' for full list of Info\n\n'WARNING: You must use the same MASTER PASSWORD for both adding and retrieving a password, otherwise the service cannot be provided!'",
bd=4,font="helvatica", wraplength=900, padx=10, pady=10)
defaultDisplay.place(anchor=CENTER, relx=0.5, rely=0.3)


root.mainloop()