import tkinter as tk
import webbrowser

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
        utton_add.pack(side=tk.RIGHT)
        window_new_query.bind("<Return>", handle_return)
        
        window_new_query.mainloop()


    button_add_query = tk.Button(text="Add new query", master=window, padx=3, pady=3, borderwidth=3)
    button_add_query.pack(side=tk.RIGHT, padx=10, pady=10)
    button_add_query.bind("<Button-1>", handle_new_query_button)

    button_notification = tk.Button(text="Simulate notification", master=window, 
            command=lambda: notification("RTX 3080", "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400", "$849.99 USD", "No"))
    button_notification.pack(side=tk.TOP, pady=10, padx=10)

    window.mainloop()

def notification(product, source, price, belowMSRP):
    # Makes the beep for a notification, but also prints a newline...
    print("\a")
    
    # Makes the window for the notification
    window_notification = tk.Tk()
    window_notification.title("Alert")
    
    frame = tk.Frame(master=window_notification)

    lbl_available = tk.Label(text="Available:", master=frame)
    lbl_name = tk.Label(text=product, master=frame)
    lbl_available.grid(row=0, column=0, sticky=tk.W)
    lbl_name.grid(row=0, column=1, sticky=tk.W)
    
    lbl_from = tk.Label(text="From:", master=frame)
    lbl_source = tk.Label(text=source, master=frame)
    lbl_from.grid(row=1, column=0, sticky=tk.W)
    lbl_source.grid(row=1, column=1, sticky=tk.W)
    lbl_source.bind("<Button-1>", lambda event: webbrowser.open(source))

    lbl_price = tk.Label(text="Price:", master=frame)
    lbl_price_listed = tk.Label(text=price, master=frame)
    lbl_price.grid(row=2, column=0, sticky=tk.W)
    lbl_price_listed.grid(row=2, column=1, sticky=tk.W)

    lbl_msrp = tk.Label(text="Below MSRP:", master=frame)
    lbl_below = tk.Label(text=belowMSRP, master=frame)
    lbl_msrp.grid(row=3, column=0, sticky=tk.W)
    lbl_below.grid(row=3, column=1, sticky=tk.W)

    frame.pack(padx=10, pady=10)
    frame.grid_columnconfigure(0, minsize=100)

    screen_width = window_notification.winfo_screenwidth()
    screen_height = window_notification.winfo_screenheight()
    
    x = screen_width - 250
    y = screen_height - 200 

    # window_notification.geometry(f"+{x}+{y}")

    def close():
        window_notification.quit()
        window_notification.destroy()
    
    window_notification.protocol("WM_DELETE_WINDOW", close)
    #window_notification.after(2000, close)
    
    window_notification.mainloop()

if __name__ == "__main__":
    launchGUI()
