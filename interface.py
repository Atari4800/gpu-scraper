import tkinter as tk
import webbrowser
import re
import json
import os
import tkinter.font as tkFont

# Creates a window
def launchGUI():
    window = tk.Tk()
    window.title("GPU-Scraper")
    
    with open("productList.json", "r") as dataFile:
        data = json.load(dataFile)

    lbl_queries_title = tk.Label(text="Current Queries", master=window)
    lbl_queries_title.pack()

    #frame_query_titles = tk.Frame(master=window) 
    #lbl_col1 = tk.Label(text="Product", master=frame_query_titles)
    #lbl_col2 = tk.Label(text="Price", master=frame_query_titles)
    #lbl_col3 = tk.Label(text="Source", master=frame_query_titles) 
    #lbl_col1.grid(row=0, column=0)
    #lbl_col2.grid(row=0, column=1)
    #lbl_col3.grid(row=0, column=2)
    
    class ProductRow:
        def __init__(self, myMaster, index):
            self.index = index
            product = data["Product"][index]

            self.name = tk.Label(text=product["productType"], master=myMaster)
            self.price = tk.Label(text="   ${:.2f}   ".format(product["productPrice"]), master=myMaster)
            self.link = tk.Label(text=shortenURL(product["productLink"]), master=myMaster)
            f = tkFont.Font(self.link, self.link.cget("font"))
            f.configure(underline = True)
            self.link.configure(font=f)

            self.link.bind("<Button-1>", lambda event: webbrowser.open(product["productLink"]))

            self.name.grid(row=self.index + 1, column=0, sticky="w")
            self.price.grid(row=self.index + 1, column=1, sticky="e")
            self.link.grid(row=self.index + 1, column=2, sticky="w")

    frame_wrapper = tk.Frame(master=window)
    frame_wrapper.pack()

    canvas_queries = tk.Canvas(master=frame_wrapper, height=200)
    frame_product_rows = tk.Frame(master=canvas_queries)
    scrollbar = tk.Scrollbar(master=frame_wrapper)

    canvas_queries.config(yscrollcommand=scrollbar.set, highlightthickness=0)
    scrollbar.config(orient=tk.VERTICAL, command=canvas_queries.yview)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    canvas_queries.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
    canvas_queries.create_window(0, 0, window=frame_product_rows, anchor=tk.NW)

    def updateScrollRegion():
        canvas_queries.update_idletasks()
        canvas_queries.config(scrollregion=frame_product_rows.bbox())

    for i in range(len(data["Product"])):
        row = ProductRow(frame_product_rows, i)

    updateScrollRegion() 

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
                # Add this product to the json file
                #os.system(f"python3 productAdder.py {entry_query_label.get()} {entry_url.get()}")
                window_new_query.destroy()
            else:
                lbl_invalid_input["text"] = "One or more fields blank"
        
        def handle_return(event):
            handle_new_query_add()

        button_add = tk.Button(text="Add", master=window_new_query, command=handle_new_query_add, padx=3, pady=3)
        button_add.pack(side=tk.RIGHT)
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
    lbl_source = tk.Label(text=shortenURL(source) + " (click here)", master=frame)
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

    frame.grid_columnconfigure(0, minsize=100)
    frame.pack(padx=10, pady=10)

    screen_width = window_notification.winfo_screenwidth()
    screen_height = window_notification.winfo_screenheight()
    
    x = screen_width - 300
    y = screen_height - 200 

    window_notification.geometry(f"+{x}+{y}")

    #window_notification.after(2000, close)
    def close():
        window_notification.quit()
        window_notification.destroy()
    
    window_notification.protocol("WM_DELETE_WINDOW", close)
    
    window_notification.mainloop()

def confirmationDialog(message, command, title="Please confirm"):
    confirmation = tk.Tk()
    confirmation.title(title)
    confirmation.resizable(width=False, height=False)

    components = tk.Frame(master=confirmation) 
    lbl_message = tk.Label(text=message, master=components)
    lbl_message.pack(pady=5)

    def close():
        confirmation.quit()
        confirmation.destroy()

    def success():
        command()
        close()
    
    frame_buttons = tk.Frame(master=components)
    button_yes = tk.Button(text="Yes", master=frame_buttons, command=success)
    button_no = tk.Button(text="No", master=frame_buttons, command=close)
    button_yes.grid(row=0, column=0)
    button_no.grid(row=0, column=1)
    for i in range(2):
        frame_buttons.columnconfigure(i, minsize=75)
    frame_buttons.pack(pady=5)

    components.pack(padx=10, pady=5)

    confirmation.mainloop()


# This function will attempt to shorten a url to produce a shorter string
def shortenURL(url):
    result = ""
    if re.search("www.bestbuy.com/", url):
        result = "Best Buy"
    elif re.search("www.newegg.com/", url):
        result = "Newegg"
    elif re.search("www.bhphotovideo.com/", url):
        result = "B&H"
    else:
        findings = re.search("http(?:s)?\:\/\/(.*\.(?:com|org|gov|net))", url)
        if findings:
            result = findings.group(0)
        else:
            result = url
    return result


if __name__ == "__main__":
    launchGUI()
