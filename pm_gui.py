import sys
from tkinter import *
from tkinter import messagebox

import pyperclip
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

nameLabel = Frame(root, relief='ridge', borderwidth=1, bg='gray80')
namePlaceHolder = Label(nameLabel, text='Password Manager') #font text or image can be changed
namePlaceHolder.pack(pady=10)
nameLabel.pack(fill=X)

# masterPass_Input_Var, masterPass_ReEnter_Input_Var, service_Input_Var, password_Input_Var, email_Input_Var, note_Input_Var = [None]*6


def defaultDisplay_Hide():

    global displayFrame
    displayFrame.pack_forget()
    # displayFrame.destroy()
    displayFrame = LabelFrame(frame1, text='', relief=FLAT, bd=3)
    displayFrame.pack(expand=True, fill=BOTH, padx=5, pady=5)



def helpDisplay():  # Button 8

    defaultDisplay_Hide()       

    defaultDisplay = Label(displayFrame,bg='silver', text=helpText,bd=4,font="helvatica", wraplength=900, padx=10, pady=10)
    defaultDisplay.pack(expand=True, fill=BOTH, padx=5, pady=5)
    # defaultDisplay.place(anchor=CENTER, relx=0.5, rely=0.3)


def showDefaultDisplay():
    defaultDisplay_Hide()  # Nascondi il frame attuale
    defaultDisplay = Label(displayFrame, bg='silver', text=
    "Password Manager by Stevees.\n\nPress any button from above to being OR 'Help' for full list of Info\n\n'WARNING: You must use the same MASTER PASSWORD for every password to add or search, otherwise the service cannot be provided!'",
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

    header_Label = Label(displayFrame, text="Add Credentials", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

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

    def credsSubmit_func(): 
        service = service_Input_Var.get()
        email = email_Input_Var.get()
        password = password_Input_Var.get()
        note = note_Input_Var.get()
        master_password = masterPass_Input_Var.get()
        master_password_confirmation = masterPass_ReEnter_Input_Var.get()

        emptyInpCheck = [masterPass_Input_Var.get(), masterPass_ReEnter_Input_Var.get(), service_Input_Var.get(), password_Input_Var.get(), email_Input_Var.get()]    
        
        #Loop to check empty or same masterpass value.
        for v in emptyInpCheck:        
            
            empyt_val = ""        

            if empyt_val in emptyInpCheck:
                messagebox.showwarning("Missing Field", "Missing one OR some fields\nPlease Re-Verify")
                break

            elif masterPass_Input_Var.get() != masterPass_ReEnter_Input_Var.get():
                messagebox.showwarning("Failed", "MASTER Password Not Matching\nPlease Re-Verify")
                # print("Not Equal Password")
                break

            elif 1 == pm.add_password(service, email, password, note, master_password):
                messagebox.showinfo("Success", "Password succesfully stored.")
                addCreds() # <- is always better idea than default as it helps user in adding multiple entries one after other
                # showDefaultDisplay()         
                break

            else:
                messagebox.showinfo("Failed", f"Error: Unable to add password. An entry with service '{service}' and email '{email}' already exists.")            
                break             

        # if master_password != master_password_confirmation:
        #     messagebox.showwarning("Failed", "MASTER Password Not Matching\nPlease Re-Verify")
        #     print("Not Equal Password")
        #     return
        
        # Calling the add_password function with the extracted values
        # if 1 == pm.add_password(service, email, password, note, master_password):
        #     messagebox.showinfo("Success", "Password succesfully stored.")
        #     showDefaultDisplay()         
        # else:
        #     messagebox.showinfo("Failed", f"Error: Unable to add password. An entry with service '{service}' and email '{email}' already exists.")
        #     return

    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=credsSubmit_func) # -> credsSubmit_func()
    credsSubmit.place(relx=0.5, rely=0.5, anchor=CENTER)

#To add real-time validation of submit button in Add New Credentiala
#     masterPass_Input_Var.trace_add("write", validate_fields)
#     masterPass_ReEnter_Input_Var.trace_add("write", validate_fields)
#     service_Input_Var.trace_add("write", validate_fields)
#     email_Input_Var.trace_add("write", validate_fields)
#     password_Input_Var.trace_add("write", validate_fields)
#     note_Input_Var.trace_add("write", validate_fields)

#     validate_fields()  

# def validate_fields(*args):
#     master_password = masterPass_Input_Var.get().strip()
#     master_password_confirmation = masterPass_ReEnter_Input_Var.get().strip()
#     service = service_Input_Var.get().strip()
#     email = email_Input_Var.get().strip()
#     password = password_Input_Var.get().strip()

#     if (master_password and master_password_confirmation and service and email and password and master_password == master_password_confirmation):
#         credsSubmit.config(state="normal")
#     else:
#         credsSubmit.config(state="disabled")



    

# Search Password # Button 2
def searchPassword():

    defaultDisplay_Hide()        

    global masterPass_Input_Var, service_Input_Var, searchPassword_Submit

    masterPass_Input_Var = StringVar()
    service_Input_Var = StringVar()        

    header_Label = Label(displayFrame, text="Search Password", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.2, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.2, anchor=CENTER, x=-35)

    service_Label = Label(displayFrame, text="Enter Service Name :")
    service_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=55)
    service_Input = Entry(displayFrame, width=30, textvariable=service_Input_Var)
    service_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    def searchPassword_func(): #2 Result Display (Search Password)
        resultWindow = Toplevel(root)
        resultWindow.geometry("750x300")
        resultWindow.title("Search Passwords")

        window_width = 750
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
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

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)
        

        service = service_Input_Var.get()

        email = pm.get_mails(service)    

        master_password = masterPass_Input_Var.get()

        if email:
            for el in email:
                psw = pm.get_password(service, el, masterPass_Input_Var.get())
                note = pm.get_note(service, el)[0]
                if psw:
                    frame_for_result = Frame(scrollable_frame)
                    frame_for_result.pack(pady=5, fill=X)
                    
                    result_label = Label(frame_for_result, text=f"Password for account '{el}' of '{service}' is: '{psw}', Note: {note}", anchor="center")
                    result_label.pack(side=LEFT, padx=5)

                    def copy_to_clipboard(password=psw):
                        pyperclip.copy(password)
                    
                    copy_button = Button(frame_for_result, text="Copy Password", command=copy_to_clipboard)
                    copy_button.pack(side=RIGHT, padx=5)
                    showDefaultDisplay()
                else:
                    Label(scrollable_frame, text=f"Error in Decrypting for account {el}! Incorrect MASTER PASSWORD.", anchor="center").pack(pady=5, fill=X)
        else:
            Label(scrollable_frame, text=f"Incorrect MASTER PASSWORD or the entry does not exist.", anchor="center").pack(pady=5, fill=X)
        
        

    searchPassword_Submit = Button(displayFrame, text='Submit', height=2, width=25, command=searchPassword_func)
    searchPassword_Submit.place(relx=0.5, rely=0.4, anchor=CENTER)    

    def validate_searhPassword(*args):        
        if masterPass_Input_Var.get() and service_Input_Var.get():
            searchPassword_Submit.config(state="normal")                    
        else:
            searchPassword_Submit.config(state="disabled")
    
    masterPass_Input_Var.trace_add("write", validate_searhPassword)
    service_Input_Var.trace_add("write", validate_searhPassword)
    validate_searhPassword()        



def modifyPassword(): # 3 Modify Password Button



    defaultDisplay_Hide()

    global old_service, old_email, old_password, old_note, new_service, new_email, new_password, new_note, master_password
    old_service, old_email, old_password, old_note, new_service, new_email, new_password, new_note, master_password = [None]*9

    header_Label = Label(displayFrame, text="Modify Password", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      
    

    service_Input_Var = StringVar()
    old_service = service_Input_Var.get()    

    service_Label = Label(displayFrame, text="Service :")
    service_Label.place(relx=0.3, rely=0.2, anchor=CENTER, x=2)
    service_Input = Entry(displayFrame, width=30, textvariable=service_Input_Var)
    service_Input.place(relx=0.4, rely=0.2, anchor=CENTER)

    email_Input_Var = StringVar()    
    old_email = email_Input_Var.get()

    email_Label = Label(displayFrame, text="Email :")
    email_Label.place(relx=0.3, rely=0.3, anchor=CENTER, x=7)
    email_Input = Entry(displayFrame, width=30, textvariable=email_Input_Var)
    email_Input.place(relx=0.4, rely=0.3, anchor=CENTER)

    old_Password_Input_Var = StringVar()
    old_password = old_Password_Input_Var.get()
    
    oldPassword_Label = Label(displayFrame, text="Old Password :")
    oldPassword_Label.place(relx=0.3, rely=0.4, anchor=CENTER, x=-13)
    oldPassword_Input = Entry(displayFrame, width=30, textvariable=old_Password_Input_Var)
    oldPassword_Input.place(relx=0.4, rely=0.4, anchor=CENTER)

    # old_Note_Input_Var = StringVar()
    # old_note = old_Note_Input_Var.get()

    # old_Note_Label = Label(displayFrame, text="Old Note :")
    # old_Note_Label.place(relx=0.3, rely=0.5, anchor=CENTER)
    # old_Note_Input = Entry(displayFrame, width=30, textvariable=old_Note_Input_Var)
    # old_Note_Input.place(relx=0.4, rely=0.5, anchor=CENTER)
    # old_Note_Input.config(state=DISABLED) #temp disable main funciton not implemented to be removed later

    new_service_Input_Var = StringVar()
    new_service = new_service_Input_Var.get()
    
    new_Service_Label = Label(displayFrame, text="New Service :")
    new_Service_Label.place(relx=0.5, rely=0.2, anchor=CENTER, x=40)
    new_Service_Input = Entry(displayFrame, width=30, textvariable=new_service_Input_Var)
    new_Service_Input.place(relx=0.6, rely=0.2, anchor=CENTER, x=50)    

    new_email_Input_Var = StringVar()
    new_email = new_email_Input_Var.get()
    
    new_email_Label = Label(displayFrame, text="New Email :")
    new_email_Label.place(relx=0.5, rely=0.3, anchor=CENTER, x=43)
    new_email_Input = Entry(displayFrame, width=30, textvariable=new_email_Input_Var)
    new_email_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=50)

    new_password_Input_Var = StringVar()
    new_password = new_password_Input_Var.get()
    
    new_Password_Label = Label(displayFrame, text="New Password :")
    new_Password_Label.place(relx=0.5, rely=0.4, anchor=CENTER, x=34)
    new_Password_Input = Entry(displayFrame, width=30, textvariable=new_password_Input_Var)
    new_Password_Input.place(relx=0.6, rely=0.4, anchor=CENTER, x=50)

    new_note_Input_Var = StringVar()
    new_note = new_note_Input_Var.get()
    
    new_note_Label = Label(displayFrame, text="New Note :")
    new_note_Label.place(relx=0.5, rely=0.5, anchor=CENTER, x=47)
    optional_Label = Label(displayFrame, text="(Optional)")
    optional_Label.place(relx=0.7, rely=0.5, anchor=CENTER, x=52)
    new_note_Input = Entry(displayFrame, width=30, textvariable=new_note_Input_Var)
    new_note_Input.place(relx=0.6, rely=0.5, anchor=CENTER, x=50)

    masterPass_Input_Var = StringVar()
    master_password = masterPass_Input_Var.get()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.5, rely=0.6, anchor=CENTER, x=-90, y=8)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show="*")
    masterPass_Input.place(relx=0.5, rely=0.6, anchor=CENTER, x=90, y=8)
    
    def validate_ModPsw(*args):
        old_service = service_Input_Var.get() 
        old_password = old_Password_Input_Var.get()
        old_email = email_Input_Var.get()
        master_password = masterPass_Input_Var.get().strip()
        new_password = new_password_Input_Var.get()
        new_email = new_email_Input_Var.get()
        new_service = new_service_Input_Var.get()
        if master_password and old_service and old_email and old_password and new_email and new_service and new_password:
            credsSubmit.config(state="normal")
        else:
            credsSubmit.config(state="disabled")

    def modifyPassword_Submit():        
        old_service = service_Input_Var.get() 
        old_password = old_Password_Input_Var.get()
        old_email = email_Input_Var.get()
        master_password = masterPass_Input_Var.get().strip()
        new_note = new_note_Input_Var.get()
        new_password = new_password_Input_Var.get()
        new_email = new_email_Input_Var.get()
        new_service = new_service_Input_Var.get()

        ret = pm.modify_entry(old_service, old_email, old_password, new_service, new_email, new_password, new_note, master_password)  
        if ret == 0:
            messagebox.showinfo("Success", f"Credentials updated.")
            showDefaultDisplay()
        elif ret == 1:
            messagebox.showinfo("Failed", "Old password is wrong. Impossible to modify the entry.")
        elif ret == 2:
            messagebox.showinfo("Failed", "Error in decrtpting. Wrong MASTER PASSWORD.")
        elif ret == 3:
            messagebox.showinfo("Failed", "No enrty to modify found.")
            



    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=modifyPassword_Submit)
    credsSubmit.place(relx=0.5, rely=0.7, anchor=CENTER)    

    service_Input_Var.trace_add("write", validate_ModPsw)
    old_Password_Input_Var.trace_add("write", validate_ModPsw)
    email_Input_Var.trace_add("write", validate_ModPsw)
    masterPass_Input_Var.trace_add("write", validate_ModPsw)
    new_password_Input_Var.trace_add("write", validate_ModPsw)
    new_email_Input_Var.trace_add("write", validate_ModPsw)
    new_service_Input_Var.trace_add("write", validate_ModPsw)
    validate_ModPsw()

  


def delEntry():
    defaultDisplay_Hide()        

    header_Label = Label(displayFrame, text="Delete a Password", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

    global masterPass_Input_Var, popResult, credsSubmit

    masterPass_Input_Var = StringVar()
    email_Input_Var = StringVar()
    service_Input_Var = StringVar()
    password_Input_Var = StringVar()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.2, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.2, anchor=CENTER, x=-35)

    service_Label = Label(displayFrame, text="Service :")
    service_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)
    service_Input = Entry(displayFrame, width=30, textvariable=service_Input_Var)
    service_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    email_Label = Label(displayFrame, text="Email :")
    email_Label.place(relx=0.4, rely=0.4, anchor=CENTER, x=35)
    email_Input = Entry(displayFrame, width=30, textvariable=email_Input_Var)
    email_Input.place(relx=0.6, rely=0.4, anchor=CENTER, x=-35)

    password_Label = Label(displayFrame, text="Password :")
    password_Label.place(relx=0.4, rely=0.5, anchor=CENTER, x=35)
    password_Input = Entry(displayFrame, width=30, textvariable=password_Input_Var)
    password_Input.place(relx=0.6, rely=0.5, anchor=CENTER, x=-35)

    def validate_delPsw(*args):
        master_password = masterPass_Input_Var.get().strip()
        if master_password and service_Input_Var.get() and email_Input_Var.get() and password_Input_Var.get():
            credsSubmit.config(state="normal")
        else:
            credsSubmit.config(state="disabled")

    def delPsw():
        confirm = messagebox.askyesno("Confirm Delete", f"ATTENTION! Are you sure to delete {email_Input_Var.get()}'s {service_Input_Var.get()} password? This operation can't be undone.")
        if confirm:
            if pm.get_password(service_Input_Var.get(), email_Input_Var.get(), masterPass_Input_Var.get()) == password_Input_Var.get():
                ret = pm.remove_entry(service_Input_Var.get(), email_Input_Var.get(), masterPass_Input_Var.get())
                if ret == 1:
                    messagebox.showinfo("Success", f"Password for service '{service_Input_Var.get()}' and email '{email_Input_Var.get()}' removed.")
                    showDefaultDisplay()
                # elif ret == 2:
                #     messagebox.showinfo("Failed", "No enrty to remove found.")
                elif ret == 0:
                    messagebox.showinfo("Failed", "Error in decrtpting. Wrong MASTER PASSWORD.")
            elif pm.get_password(service_Input_Var.get(), email_Input_Var.get(), masterPass_Input_Var.get()) == None:
                messagebox.showinfo("Failed", "Error in decrtpting. Wrong MASTER PASSWORD or service or email.")
            else:
                messagebox.showinfo("Failed", "Wrong password. Cant't delete the entry.")

    credsSubmit = Button(displayFrame, text='Submit',height=2, width=25, command=delPsw)
    credsSubmit.place(relx=0.5, rely=0.6, anchor=CENTER)        
    masterPass_Input_Var.trace_add("write", validate_delPsw)
    email_Input_Var.trace_add("write", validate_delPsw)
    service_Input_Var.trace_add("write", validate_delPsw)
    password_Input_Var.trace_add("write", validate_delPsw)
    validate_delPsw()
    


def viewAll():  # 5 View All Database

    defaultDisplay_Hide()        

    global masterPass_Input_Var, credsSubmit
    masterPass_Input_Var = StringVar()

    header_Label = Label(displayFrame, text="View All Database", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    def validate_viewAll(*args):
        master_password = masterPass_Input_Var.get().strip()
        if master_password:
            credsSubmit.config(state="normal")
        else:
            credsSubmit.config(state="disabled")

    def printAll(**kwargs): #5 Result Display (View All)

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

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)

        Label(scrollable_frame, text="Result", font=('Helvetica 17 bold'), anchor="center").pack(pady=10, fill=X, expand=True)

        popResult = masterPass_Input_Var.get()
        result = pm.print_all(popResult)
        


        if result:
            for el in result:
                frame_row = Frame(scrollable_frame)
                frame_row.pack(fill=X, pady=5)
                
                label_text = f"Service: '{el[0]}', Email: '{el[1]}', Password: '{el[2]}', Note: {el[3]}"
                Label(frame_row, text=label_text, anchor="center").pack(side=LEFT, fill=X, expand=True)

                if el[2] != "---":
                    copy_button = Button(frame_row, text="Copy Password", command=lambda psw=el[2]: pyperclip.copy(psw))
                    copy_button.pack(side=RIGHT, padx=10)
                    showDefaultDisplay()  
                else:
                    Label(frame_row, text="Decryption Error", fg="red", anchor="center").pack(side=RIGHT, padx=10)
        else:
            Label(scrollable_frame, text="No results found or incorrect master password.", anchor="center").pack(pady=10, fill=X)
        
         


    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=printAll)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)

    masterPass_Input_Var.trace_add("write", validate_viewAll)
    validate_viewAll()







def searchByEmail(): #6

    defaultDisplay_Hide()        

    global masterPass_Input_Var, email_Input_Var

    header_Label = Label(displayFrame, text="Search by Email", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

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

    def validate_searchByEmail(*args):
        master_password = masterPass_Input_Var.get().strip()
        email = email_Input_Var.get().strip()
        if master_password and email:
            credsSubmit.config(state="normal")
        else:
            credsSubmit.config(state="disabled")

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

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)

        if result:
            for el in result:
                frame_row = Frame(scrollable_frame)
                frame_row.pack(fill=X, pady=5)

                label_text = f"Service: '{el[0]}', Email: '{el[1]}', Password: '{el[2]}', Note: {el[3]}"
                Label(frame_row, text=label_text, anchor="center").pack(side=LEFT, fill=X, expand=True)

                if el[2] != "---":
                    copy_button = Button(frame_row, text="Copy Password", command=lambda psw=el[2]: pyperclip.copy(psw))
                    copy_button.pack(side=RIGHT, padx=10)
                    showDefaultDisplay()
                else:
                    Label(frame_row, text="Decryption Error", fg="red", anchor="center").pack(side=RIGHT, padx=10)
        else:
            Label(scrollable_frame, text="No results found or incorrect master password.", anchor="center").pack(pady=10, fill=X)


           

    credsSubmit = Button(displayFrame, text='Submit', height=2, width=25, command=credsSubmit_func)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)
    masterPass_Input_Var.trace_add("write", validate_searchByEmail)
    email_Input_Var.trace_add("write", validate_searchByEmail)

    validate_searchByEmail()


def delDatabase():
    defaultDisplay_Hide()        

    header_Label = Label(displayFrame, text="Delete the entire Database", font=('Helvetica 14 bold underline')).place(relx=0.5, rely=0.1, anchor=CENTER)      

    global masterPass_Input_Var, popResult, credsSubmit
    masterPass_Input_Var = StringVar()

    masterPass_Label = Label(displayFrame, text="Enter MASTER PASSWORD :")
    masterPass_Label.place(relx=0.4, rely=0.3, anchor=CENTER, x=35)
    masterPass_Input = Entry(displayFrame, width=30, textvariable=masterPass_Input_Var, show='*')
    masterPass_Input.place(relx=0.6, rely=0.3, anchor=CENTER, x=-35)

    def validate_delDatabase(*args):
        master_password = masterPass_Input_Var.get().strip()
        if master_password:
            credsSubmit.config(state="normal")
        else:
            credsSubmit.config(state="disabled")

    def delAll():
        confirm = messagebox.askyesno("Confirm Delete", "ATTENTION! This operation can't be undone. All datas will be lost. Are you sure you want to delete the entire database?")
        if confirm:
            if pm.delete_all(masterPass_Input.get()) == 1:
                messagebox.showinfo("Success", "Database succesfully deleted.")
                showDefaultDisplay()
            else:
                messagebox.showinfo("Failed", f"Error: Unable to delete database. Try again.")
            
    credsSubmit = Button(displayFrame, text='Submit',height=2, width=25, command=delAll)
    credsSubmit.place(relx=0.5, rely=0.4, anchor=CENTER)        
    masterPass_Input_Var.trace_add("write", validate_delDatabase)
    validate_delDatabase()

def quit():
    sys.exit(0)


pm.create_db()

#menu icons / buttons
menuButtons = Frame(root, relief='groove', borderwidth=1, bg='gray70', height=80)

menuButton1 = Button(menuButtons, text='Add New Credentials', height=2, width=15, command=addCreds).place(relx=0.1, rely=0.5, anchor=CENTER)
menuButton2 = Button(menuButtons, text='Search a Password', height=2, width=15, command=searchPassword).place(relx=0.2, rely=0.5, anchor=CENTER)
menuButton3 = Button(menuButtons, text='Modify a Password', height=2, width=15, command=modifyPassword).place(relx=0.3, rely=0.5, anchor=CENTER)
menuButton4 = Button(menuButtons, text='Delete a Password', height=2, width=15, command=delEntry).place(relx=0.4, rely=0.5, anchor=CENTER)
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


helpText="Choose the desired service by selecting the corresponding buttons from above."'\n''\n'"WARNING: You must use the same MASTER PASSWORD for every password to add or search, otherwise the service cannot be provided!"'\n''\n'"You will need to remember the MASTER PASSWORD, as it cannot be stored in the database."'\n''\n'"In the email field, you can enter either the email address used for that account or a Username or UserID."'\n''\n'"You can modify the service, email, password, and/or notes for each entry. The operation OVERWRITES the old data."'\n''\n'"You can delete an entry by confirming the service, email, and password, losing the respective information PERMANENTLY."

defaultDisplay = Label(displayFrame, bg='silver', text=
"Password Manager by Stevees.\n\nPress any button from above to being OR 'Help' for full list of Info\n\n'WARNING: You must use the same MASTER PASSWORD for every password to add or search, otherwise the service cannot be provided!'",
bd=4,font="helvatica", wraplength=900, padx=10, pady=10)
defaultDisplay.place(anchor=CENTER, relx=0.5, rely=0.3)


root.mainloop()