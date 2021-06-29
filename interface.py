import tkinter as tk
import os

# This method is called when the user clicks the add new query button on the interface's main page
def handle_new_query_button(event):        
    window_new_query = tk.Tk()
    window_new_query.title("Create new Query")
    
    frame_fields = tk.Frame(master=window_new_query)
    frame_fields.pack()
    
    lbl_enter_url = tk.Label(text="Product link:", master=frame_fields)
    lbl_enter_url.grid(row=0, column=0)
    
    entry_url = tk.Entry(width=40, master=frame_fields)
    entry_url.grid(row=0, column=1)
    
    lbl_query_label = tk.Label(text="Query label:", master=frame_fields)
    lbl_query_label.grid(row=1, column=0)
    
    entry_query_label = tk.Entry(width=40, master=frame_fields)
    entry_query_label.grid(row=1, column=1)
    
    lbl_invalid_input = tk.Label(text="", foreground="red", master=window_new_query)
    lbl_invalid_input.pack()
    
    # This method is called when the adding query window add button is clicked.
    def handle_new_query_add():
        if entry_url.get() != "" and entry_query_label.get() != "":
            # Add code here to create a new Query and add it to the Query collection
            
            window_new_query.destroy()
        else:
            lbl_invalid_input["text"] = "One or more fields blank"
            
    def handle_return(event):
        handle_new_query_add()
    
    button_add = tk.Button(text="Add", master=window_new_query, command=handle_new_query_add, padx=3, pady=3)
    button_add.pack(side=tk.RIGHT)
    window_new_query.bind("<Return>", handle_return)
    
    window_new_query.mainloop()

# Creates a window
def launchGUI():
    window = tk.Tk()
    window.title("GPU-Scraper")

    frame_queries = tk.Frame(master=window)
    lbl_queries_title = tk.Label(text="Current Queries", master=frame_queries)
    lbl_queries_title.pack()

    lbl_no_queries = tk.Label(text="You have no queries.", master=frame_queries)
    lbl_no_queries.pack()

    frame_queries.pack()

    button_add_query = tk.Button(text="Add new query", master=window, padx=3, pady=3, borderwidth=3)
    button_add_query.pack(side=tk.RIGHT, padx=10, pady=10)
    button_add_query.bind("<Button-1>", handle_new_query_button)

    button_notification = tk.Button(text="Simulate notification", master=window, 
            command=lambda: notification("RTX 3080", "Best Buy", "$699.99 USD", "Yes"))
    button_notification.pack(side=tk.TOP, pady=10, padx=10)

    window.mainloop()

def notification(product, source, price, belowMSRP):
    # Makes the beep for a notification, but also prints a newline...
    print("\a")
    
    # Makes the window for the notification
    window_notification = tk.Tk()
    window_notification.title("Alert")
    
    lbl_info = tk.Label(text=f"Available: {product}\nFrom: {source}\nPrice: {price}\nBelow MSRP: {belowMSRP}", master=window_notification, justify=tk.LEFT, padx=30, pady=20)
    lbl_info.pack()    

    screen_width = window_notification.winfo_screenwidth()
    screen_height = window_notification.winfo_screenheight()
    
    x = screen_width - 250
    y = screen_height - 200 

    window_notification.geometry(f"+{x}+{y}")

    def close():
        window_notification.quit()
        window_notification.destroy()
    
    window_notification.protocol("WM_DELETE_WINDOW", close)
    #window_notification.after(2000, close)
    
    window_notification.mainloop()

if __name__ == "__main__":
    launchGUI()
