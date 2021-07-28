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


class ProductRow:
    """
    This class handles everything related to a single row in the current
    queries table on the main page of the GUI. An instance of this 
    object displays the specified information about a single product,
    makes, and handles any related buttons.
    """

    rows = 0
    """
    Static class variable to count how many instances of ProductRow have
    been made.
    """

    refresh = lambda: print("Meaningless refresh")
    """
    refresh is a function that it calls after deleting an item to properly
    call the updateScrollRegion method and shrink the scrolling region.
    """

    def __init__(self, myMaster):
        """
        Creates a new ProductRow, handling a whole row in the current
        queries table.

        :type myMaster: string
        :param myMaster: The name of this component's master component

        :type index: int
        :param index: The index of this row in the table. The first row
        has index 0, the second is index 1, and so on.
        """
        self.row = ProductRow.rows

        with open("productList.json", "r") as dataFile:
            data = json.load(dataFile)

        product = data["Product"][self.row]

        self.label = product["productType"]
        self.url = product["productLink"]

        self.name = tk.Label(text=self.label, master=myMaster,
                             width=15, anchor="w")
        self.price = tk.Label(text="   ${:.2f}   ".format(
            product["productPrice"]), master=myMaster)
        self.link = tk.Label(text=shortenURL(self.url),
                             master=myMaster)
        f = tk_font.Font(self.link, self.link.cget("font"))
        f.configure(underline=True)
        self.link.configure(font=f)

        self.link.bind("<Button-1>",
                       lambda event: webbrowser.open(product["productLink"]))

        def delete_me(event):
            base = item_base.item_base()
            base.del_item(url=self.url,
                         json_file="productList.json")
            self.self_destruct()

        self.delete = tk.Button(text="Delete", master=myMaster)
        self.delete.bind("<Button-1>", delete_me)

        self.name.grid(row=self.row + 1, column=0, sticky="w")
        self.price.grid(row=self.row + 1, column=1, sticky="e")
        self.link.grid(row=self.row + 1, column=2, sticky="w")
        self.delete.grid(row=self.row + 1, column=3, sticky="e")

        myMaster.grid_columnconfigure(index=3, minsize=85)

        ProductRow.rows += 1

    def self_destruct(self):
        self.name.destroy()
        self.price.destroy()
        self.link.destroy()
        self.delete.destroy()
        ProductRow.refresh()


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
    #     │   └── frame_product_rows (Frame)
    #     └── scrollbar (Scrollbar)
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
        """
        Updates the scrolling region so it includes the current components. If
        any components were added to the scrolling region (from an add new query
        action for example), calling this method would make the region display
        the new components.
        """
        canvas_queries.update_idletasks()
        canvas_queries.config(scrollregion=frame_product_rows.bbox())

    lbl_col1 = tk.Label(text="Product", master=frame_product_rows)
    lbl_col2 = tk.Label(text="Price", master=frame_product_rows)
    lbl_col3 = tk.Label(text="Source", master=frame_product_rows)
    lbl_col1.grid(row=0, column=0)
    lbl_col2.grid(row=0, column=1)
    lbl_col3.grid(row=0, column=2)

    ProductRow.refresh = updateScrollRegion

    with open("productList.json", "r") as dataFile:
        data = json.load(dataFile)
    for i in range(len(data["Product"])):
        row = ProductRow(frame_product_rows)

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

        frame_content = tk.Frame(master=window_new_query)
        frame_content.pack(padx=10, pady=10)

        frame_fields = tk.Frame(master=frame_content)
        frame_fields.pack()

        lbl_enter_url = tk.Label(text="Product link:", master=frame_fields)
        lbl_enter_url.grid(column=0, row=0)

        entry_url = tk.Entry(width=40, master=frame_fields)
        entry_url.grid(column=1, row=0)

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
                lbl_invalid_input["text"] = "URL is empty"
            elif shortenURL(entry_url.get()) == "Other":
                lbl_invalid_input["text"] = "URL is invalid or unsupported"
            else:
                # Add this product to the json file
                adder = item_base.item_base
                result = adder.add_item(url=entry_url.get(), title=None, price=None, json_file="productList.json")
                if result == 1:
                    messageDialog("Successful addition!", "Success")
                    ProductRow(frame_product_rows)
                    updateScrollRegion()

                    window_new_query.quit()
                    window_new_query.destroy()
                else:
                    lbl_invalid_input["text"] = f"addItem error: {result}"

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

    # window_notification.after(2000, close)

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


def confirmationDialog(message, command, title="Please confirm"):
    """
    Creates a confirmation dialog. This is a simple dialog which displays a 
    single line of text, a yes button, and a no button. It is used when
    it is useful to make sure the user wants to perform some critical action
    before actually executing that action. For example, if there was a button
    on the GUI to delete a query, it would be appropriate to use a confirmation
    dialog to make sure they really want to delete the query before deleting it.

    :type message: string
    :param message: The text message displayed to the user
    
    :type command: function
    :param command: This function is called if the user presses the okay button
    
    :type title: string
    :param title: The title of the window

    :return: returns nothing
    """

    confirmation = tk.Tk()
    confirmation.title(title)
    confirmation.resizable(width=False, height=False)

    components = tk.Frame(master=confirmation)
    lbl_message = tk.Label(text=message, master=components)
    lbl_message.pack(pady=5)

    def close():
        """The code to be run when the window is closed"""
        confirmation.quit()
        confirmation.destroy()

    def success():
        """The code to be run when the user presses yes"""
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
