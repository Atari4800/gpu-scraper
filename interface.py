"""
This file handles the GUI component of our application. It is 
responsible for creating the main GUI and related components like popup
windows or notifications.
"""

import tkinter as tk
import webbrowser
import re
import json
import sys
import subprocess
import tkinter.font as tk_font

import item_base
import scheduler

class ProductGrid(tk.Frame):
    """
    One instance of this class handles all data and visual components for the 
    query table in the main interface screen. It creates a grid of information,
    where each row has the information and buttons for a single product.
    """

    refresh = lambda: print("filler refresh")

    def __init__(self, master):
        """
        Creates a grid in the main interface page.
        
        :type master: string
        :param master: The tkinter container which is a master of this grid.
        """
        super().__init__(master)
        self.pack()

        self.rows = []
        self.num_rows_created = 0
        self.num_rows = 0
        self.load_json()

        for r in range(self.num_products):
            self.add_row()

    def load_json(self):
        """
        Updates this instance's data from the file productList.json
        
        :return: returns nothing
        """
        with open("productList.json", "r") as dataFile:
            self.data = json.load(dataFile)
        self.num_products = len(self.data["Product"])

    def add_row(self):
        """
        Adds a row to the table. The object has data to keep track of which 
        product should be displayed in the next row.

        :return: returns nothing
        """
        row_num = self.num_rows_created 
        row = []
        product_data = self.data["Product"][self.num_rows]
        row.append(product_data["productLink"])
        row.append(row_num)
        
        name = tk.Label(self, text=product_data["productType"], width=15, anchor="w")
        name.grid(row=row_num, column=0)
        row.append(name)
        
        price = tk.Label(text="   ${:.2f}   ".format(
            product_data["productPrice"]), master=self)
        price.grid(row=row_num, column=1, sticky="e")
        row.append(price)

        link = tk.Label(text=shortenURL(url=row[0]), master=self)
        f = tk_font.Font(link, link.cget("font"))
        f.configure(underline=True)
        link.configure(font=f)
        link.bind("<Button-1>", lambda event: webbrowser.open(row[0]))
        link.grid(row=row_num, column=2, sticky="w")
        row.append(link)

        delete = tk.Button(self, text="Delete", command=lambda r=row: self.delete_row(r))
        delete.grid(row=row_num, column=3, sticky="e")
        self.columnconfigure(3, minsize=85)
        
        row.append(delete)

        self.rows.append(row)
        self.num_rows_created += 1
        self.num_rows += 1

    def delete_row(self, row):
        """
        Deletes the given row from the table.
        
        :param row: An entire row in the table. It should be a List with all
        of the components in that row.

        :return: returns nothing
        """
        item_base.item_base.del_item(url=row[0], json_file="productList.json")
        self.load_json()
        
        for i in range(len(row)):
            if i > 1:
                row[i].destroy()
        self.rows.remove(row)
        self.num_rows -= 1

        ProductGrid.refresh()
        

def launchGUI():
    """
    Launches the main GUI window for our application. It displays 
    information about current queries and allows the user to create a 
    new query (but does not yet actually add the query, it just shows
    the GUI component is ready)

    :return: returns nothing
    """

    # Main window root and giving it a title and some text
    window = tk.Tk()
    window.title("GPU Hunter")
    window.resizable(width=False, height=False)

    lbl_queries_title = tk.Label(text="Current Product Searches", master=window)
    lbl_queries_title.pack()

    # Creates the necessary structure of containers for the scrolling
    # The container structure is as follows:
    # window (Tk)
    # └── frame_wrapper (Frame)
    #     ├── canvas_queries (Canvas)
    #     │   └── frame_product_rows (ProductGrid)
    #     └── scrollbar (Scrollbar)
    frame_wrapper = tk.Frame(master=window)
    frame_wrapper.pack()

    canvas_queries = tk.Canvas(master=frame_wrapper, height=200)
    frame_product_rows = ProductGrid(master=canvas_queries)
    scrollbar = tk.Scrollbar(master=frame_wrapper)

    canvas_queries.config(yscrollcommand=scrollbar.set, highlightthickness=0)
    scrollbar.config(orient=tk.VERTICAL, command=canvas_queries.yview)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    canvas_queries.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
    canvas_queries.create_window(0, 0, window=frame_product_rows, anchor=tk.NW)

    def updateScrollRegion():
        """
        Updates the scrolling region so it includes the current components. If
        any components were added to the scrolling region (from an add new query
        action for example), calling this method would make the region display
        the new components.
        """
        canvas_queries.update_idletasks()
        canvas_queries.config(scrollregion=frame_product_rows.bbox())

    ProductGrid.refresh = updateScrollRegion
    updateScrollRegion()

    def handle_new_query_button(event):
        """
        Creates a separate window to get user input for a new query. It will
        ask for a url and a product name. If the user presses add and the 
        input is clearly invalid (i.e. one or both of the fields is blank), 
        it will display an error message and will not close the window. If
        the user input is valid, it closes the window.
        """
        window_new_query = tk.Tk()
        window_new_query.title("Create new Query")
        window_new_query.resizable(width=False, height=False)

        frame_content = tk.Frame(master=window_new_query)
        frame_content.pack(padx=10, pady=10)

        frame_fields = tk.Frame(master=frame_content)
        frame_fields.pack()

        lbl_enter_url = tk.Label(text="Product link:", master=frame_fields)
        lbl_enter_url.grid(column=0, row=0, sticky='W')
        entry_url = tk.Entry(width=40, master=frame_fields)
        entry_url.grid(column=1, row=0)

        lbl_enter_name = tk.Label(text="Product name:", master=frame_fields)
        lbl_enter_name.grid(column=0, row=1, sticky='W')
        entry_name = tk.Entry(width=40, master=frame_fields)
        entry_name.grid(column=1, row=1)

        lbl_enter_price = tk.Label(text="Product MSRP:", master=frame_fields)
        lbl_enter_price.grid(column=0, row=2, sticky='W')
        entry_price = tk.Entry(width=40, master=frame_fields)
        entry_price.grid(column=1, row=2)

        lbl_invalid_input = tk.Label(text="", foreground="red", master=frame_content)
        lbl_invalid_input.pack()

        def handle_new_query_add():
            """
            When the add button is pressed in the window to get input for a new
            query, it will call this method which validates the user input
            (makes sure that both fields are nonempty). If input is valid, it
            will close the dialog. If input is invalid, it will display an 
            error message and not close the window.
            """

            lbl_invalid_input["text"] = "Processing request..."

            if entry_url.get() == "":
                lbl_invalid_input["text"] = "Product link is a required field."
            elif shortenURL(entry_url.get()) == "Other":
                lbl_invalid_input["text"] = "URL is invalid or unsupported."
            else:
                # Add this product to the json file
                title = None
                msrp = None
                success = True
                if entry_name.get() != "":
                    title = entry_name.get()

                if entry_price.get() != "":
                    msrp = 0.0
                    try:
                        msrp = float(entry_price.get())
                    except:
                        lbl_invalid_input["text"] = "Entered price is not a double."
                        success = False
                if success:
                    result = item_base.item_base.add_item(url=entry_url.get(), 
                            title=title, price=msrp, json_file="productList.json")
                    if result == 1:
                        messageDialog("Successful addition!", "Success")
                        frame_product_rows.load_json()
                        frame_product_rows.add_row()
                        updateScrollRegion()

                        window_new_query.quit()
                        window_new_query.destroy()
                    else:
                        message = ""
                        if result == -6:
                            message = "Scraper cannot find price. You must manually enter the MSRP."
                        elif result == -5:
                            message = "There is a duplicate link in the JSON file."
                        elif result == -4:
                            message = "The URL is not supported."
                        elif result == -3:
                            message = "The domain cannot be reached."
                        elif result == -2:
                            message = "There is a problem opening the JSON file."
                        elif result == -1:
                            message = "The item cannot be found."
                        elif result == 0:
                            messate = "The item cannot be added to the JSON file."
                        lbl_invalid_input["text"] = message

        button_add = tk.Button(text="Add", master=frame_content, command=handle_new_query_add, padx=3)
        button_add.pack(side=tk.RIGHT)
        window_new_query.bind("<Return>", lambda event: handle_new_query_add())

        window_new_query.mainloop()

    button_add_query = tk.Button(text="Add new query", master=window, padx=3, pady=3, borderwidth=3)
    button_add_query.pack(side=tk.RIGHT, padx=10, pady=10)
    button_add_query.bind("<Button-1>", handle_new_query_button)

    button_go_now = tk.Button(text="Search now!", master=window, borderwidth=3, padx=3, pady=3)
    button_go_now.pack(side=tk.RIGHT)
    button_go_now.bind("<Button-1>", lambda event: subprocess.run([sys.executable, "initiator.py"]))

    button_scheduler = tk.Button(text="Set up Scheduler", master=window, padx=3, pady=3, borderwidth=3)
    button_scheduler.pack(side=tk.RIGHT, padx=10)

    def add_scheduler_window():
        """
        Makes a window to minutes input from user and call Scheduler with the
        input minutes.
        
        :return: returns nothing
        """
        scheduler_root = tk.Tk()
        scheduler_root.resizable(width=False, height=False)
        scheduler_root.title("Make cronjob")

        input_frame = tk.Frame(master=scheduler_root)
        input_frame.pack(padx=10, pady=10)
        lbl = tk.Label(master=input_frame, text="Scheduler minutes: ")
        lbl.pack(anchor='w')
        entry = tk.Entry(master=input_frame, width=20)
        entry.pack()
        error_message = tk.Label(master=input_frame, text="", foreground="red")
        error_message.pack()
        bttn = tk.Button(master=input_frame, text="Enter")
        bttn.pack(anchor='e')
        
        def enter_bttn():
            """
            Updates the window based on the input value. Validates the input 
            string. If input is valid, it calls Scheduler and closes the 
            window. If input is invalid, it displays an appropriate error 
            message in the same window.

            :return: returns nothing
            """
            if entry.get() == "":
                error_message["text"] = "Scheduler minutes is a required field."
            else:
                success = True
                minutes = 0
                try:
                    minutes = int(entry.get())
                except:
                    success = False
                if success and minutes <= 0:
                    error_message["text"] = "Scheduler minutes must be positive."
                elif success and minutes >= 60:
                    error_message["text"] = "Scheduler minutes cannot be greater than 59."
                elif success:
                    scheduler.Scheduler(minutes)
                    scheduler_root.quit()
                    scheduler_root.destroy()
                else:
                    error_message["text"] = "Scheduler minutes is not an integer."
                 
        bttn.bind("<Button-1>", lambda event: enter_bttn())
        scheduler_root.bind("<Return>", lambda event: enter_bttn())

        scheduler_root.mainloop()
    
    button_scheduler.bind("<Button-1>", lambda event: add_scheduler_window())

    window.mainloop()


def notification(product, source, price, belowMSRP):
    """
    Creates a notification window in the bottom right hand side of the user's
    screen. It will display the given information and does not close
    automatically.

    :type product: string
    :param product: The product available
    
    :type source: string
    :param source: The url of the product
    
    :type price: string
    :param price: The price of the product

    :type belowMSRP: string
    :param belowMSRP: Whether or not the product is below its MSRP
    
    :return: returns nothing
    """
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

    def close():
        """
        This method is called when the user closes the notification window.
        It makes sure that everything in the window is properly shut off.
        The motivation was to address an error that was occuring when the
        notification automatically closed after a given amount of time, but
        it no longer closes automatically.
        """
        window_notification.quit()
        window_notification.destroy()

    window_notification.protocol("WM_DELETE_WINDOW", close)
    window_notification.mainloop()

def shortenURL(url):
    """
    This standalone function will attempt to return a shorter version of th 
    given url. This is useful for displaying the source of a query to the user
    for a situation like a GUI or notification where the full url might require
    too much space.

    :type url: string
    :param url: The url to attempt to shorten

    :return: 
    If the url is for one of the websites we are focusing on, it returns the
    name of that business.

    A best buy url would return 'Best Buy'
    A Newegg url would return 'Newegg'
    A B&H url would return 'B&H'
    
    Otherwise, would return 'Other'
    """

    result = "Other"
    if re.search("www.bestbuy.com/", url):
        result = "Best Buy"
    elif re.search("www.newegg.com/", url):
        result = "Newegg"
    elif re.search("www.bhphotovideo.com/", url):
        result = "B&H"
    return result


def messageDialog(message, title="Message"):
    """
    Creates a dialog to display a brief textual message to the user. Useful
    for communicating error messages or success messages to the user.

    :type message: string
    :param message: The textual message to be displayed inside the window

    :type title: string
    :param title: The optional title of the dialog window
    """
    message_window = tk.Tk()
    message_window.title(title)
    message_window.resizable(width=False, height=False)

    lbl = tk.Label(text=message, master=message_window)
    lbl.pack(padx=10, pady=10)

if __name__ == "__main__":
    launchGUI()
