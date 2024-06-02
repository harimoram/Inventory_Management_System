import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

connection = None
root = None
login_window = None
username_entry = None
password_entry = None
read_window = None
update_window = None
delete_window = None

def connect_to_database(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="inventory_management"
        )
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'+{x}+{y}')

def create_item():
    global connection

    def add_item_to_db():
        name = name_entry.get()
        description = description_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        try:
            cursor = connection.cursor()
            query = "INSERT INTO items (name, description, quantity, price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, description, quantity, price))
            connection.commit()
            messagebox.showinfo("Success", "Item created successfully")
            create_window.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error creating item: {e}")

    create_window = tk.Tk()
    create_window.title("Create Item")
    center_window(create_window)
    create_window.config(bg="#f0f0f0")
    create_window.attributes("-alpha", 0.9)

    border_color = "#3498db"
    tk.Frame(create_window, width=400, height=300, bg=border_color).pack(padx=10, pady=10)

    name_label = tk.Label(create_window, text="Name:", bg="#f0f0f0")
    name_label.place(x=30, y=30)
    name_entry = tk.Entry(create_window)
    name_entry.place(x=150, y=30)

    description_label = tk.Label(create_window, text="Description:", bg="#f0f0f0")
    description_label.place(x=30, y=70)
    description_entry = tk.Entry(create_window)
    description_entry.place(x=150, y=70)

    quantity_label = tk.Label(create_window, text="Quantity:", bg="#f0f0f0")
    quantity_label.place(x=30, y=110)
    quantity_entry = tk.Entry(create_window)
    quantity_entry.place(x=150, y=110)

    price_label = tk.Label(create_window, text="Price:", bg="#f0f0f0")
    price_label.place(x=30, y=150)
    price_entry = tk.Entry(create_window)
    price_entry.place(x=150, y=150)

    create_button = tk.Button(create_window, text="Create", command=add_item_to_db, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0, highlightbackground=border_color)
    create_button.place(x=150, y=200)

    create_window.mainloop()

def read_item():
    global connection, read_window

    def on_search():
        item_id = item_id_entry.get()
        name = name_entry.get()

        try:
            cursor = connection.cursor()
            if item_id:
                query = "SELECT * FROM items WHERE item_id = %s"
                cursor.execute(query, (item_id,))
            elif name:
                query = "SELECT * FROM items WHERE name = %s"
                cursor.execute(query, (name,))
            else:
                messagebox.showwarning("Warning", "Please provide either Item ID or Name.")
                return

            item = cursor.fetchone()
            if item:
                messagebox.showinfo("Item Found", f"Item Details:\n\nID: {item[0]}\nName: {item[1]}\nDescription: {item[2]}\nQuantity: {item[3]}\nPrice: {item[4]}")
            else:
                messagebox.showinfo("Item Not Found", "No item found with the given criteria.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error reading item: {e}")

        read_window.destroy()

    read_window = tk.Tk()
    read_window.title("Read Item")
    center_window(read_window)
    read_window.config(bg="#f0f0f0")
    read_window.attributes("-alpha", 0.9)

    border_color = "#3498db"
    tk.Frame(read_window, width=400, height=150, bg=border_color).pack(padx=10, pady=10)

    item_id_label = tk.Label(read_window, text="Item ID:", bg="#f0f0f0")
    item_id_label.place(x=30, y=30)
    item_id_entry = tk.Entry(read_window)
    item_id_entry.place(x=150, y=30)

    name_label = tk.Label(read_window, text="Name:", bg="#f0f0f0")
    name_label.place(x=30, y=70)
    name_entry = tk.Entry(read_window)
    name_entry.place(x=150, y=70)

    search_button = tk.Button(read_window, text="Search", command=on_search, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0, highlightbackground=border_color)
    search_button.place(x=150, y=110)

    read_window.mainloop()

def update_item():
    global connection, update_window

    def on_update():
        item_id = item_id_entry.get()
        new_quantity = new_quantity_entry.get()

        try:
            cursor = connection.cursor()
            query = "UPDATE items SET quantity = %s WHERE item_id = %s"
            cursor.execute(query, (new_quantity, item_id))
            connection.commit()
            messagebox.showinfo("Success", "Item updated successfully")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error updating item: {e}")

        update_window.destroy()

    update_window = tk.Tk()
    update_window.title("Update Item")
    center_window(update_window)
    update_window.config(bg="#f0f0f0")
    update_window.attributes("-alpha", 0.9)

    border_color = "#3498db"
    tk.Frame(update_window, width=400, height=150, bg=border_color).pack(padx=10, pady=10)

    item_id_label = tk.Label(update_window, text="Item ID:", bg="#f0f0f0")
    item_id_label.place(x=30, y=30)
    item_id_entry = tk.Entry(update_window)
    item_id_entry.place(x=150, y=30)

    new_quantity_label = tk.Label(update_window, text="New Quantity:", bg="#f0f0f0")
    new_quantity_label.place(x=30, y=70)
    new_quantity_entry = tk.Entry(update_window)
    new_quantity_entry.place(x=150, y=70)

    update_button = tk.Button(update_window, text="Update", command=on_update, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0, highlightbackground=border_color)
    update_button.place(x=150, y=110)

    update_window.mainloop()

def delete_item():
    global connection, delete_window

    def on_delete():
        item_id = item_id_entry.get()
        name = name_entry.get()

        try:
            cursor = connection.cursor()
            if item_id:
                query = "SELECT * FROM items WHERE item_id = %s"
                cursor.execute(query, (item_id,))
            elif name:
                query = "SELECT * FROM items WHERE name = %s"
                cursor.execute(query, (name,))
            else:
                messagebox.showwarning("Warning", "Please provide either Item ID or Name.")
                return

            item = cursor.fetchone()
            if item:
                confirm_delete_window = tk.Tk()
                confirm_delete_window.title("Confirm Delete")
                center_window(confirm_delete_window)
                confirm_delete_window.config(bg="#f0f0f0")
                confirm_delete_window.attributes("-alpha", 0.9)

                border_color = "#3498db"
                tk.Frame(confirm_delete_window, width=400, height=200, bg=border_color).pack(padx=10, pady=10)

                details_label = tk.Label(confirm_delete_window, text="Item Details:", bg="#f0f0f0")
                details_label.place(x=30, y=60)
                details_text = tk.Text(confirm_delete_window, width=50, height=5)
                details_text.place(x=30, y=60)
                details_text.insert(tk.END, f"Item ID: {item[0]}\nName: {item[1]}\nDescription: {item[2]}\nQuantity: {item[3]}\nPrice: {item[4]}")

                def confirm_delete():
                    try:
                        query = "DELETE FROM items WHERE item_id = %s"
                        cursor.execute(query, (item_id,))
                        connection.commit()
                        messagebox.showinfo("Success", "Item deleted successfully")
                    except mysql.connector.Error as e:
                        messagebox.showerror("Error", f"Error deleting item: {e}")

                    confirm_delete_window.destroy()
                    delete_window.destroy()

                confirm_button = tk.Button(confirm_delete_window, text="Confirm Delete", command=confirm_delete, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0, highlightbackground=border_color)
                confirm_button.place(x=150, y=150)

                confirm_delete_window.mainloop()
            else:
                messagebox.showinfo("Item Not Found", "No item found with the given criteria.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error deleting item: {e}")

    delete_window = tk.Tk()
    delete_window.title("Delete Item")
    center_window(delete_window)
    delete_window.config(bg="#f0f0f0")
    delete_window.attributes("-alpha", 0.9)

    border_color = "#3498db"
    tk.Frame(delete_window, width=400, height=150, bg=border_color).pack(padx=10, pady=10)

    item_id_label = tk.Label(delete_window, text="Item ID:", bg="#f0f0f0")
    item_id_label.place(x=30, y=30)
    item_id_entry = tk.Entry(delete_window)
    item_id_entry.place(x=150, y=30)

    name_label = tk.Label(delete_window, text="Name:", bg="#f0f0f0")
    name_label.place(x=30, y=70)
    name_entry = tk.Entry(delete_window)
    name_entry.place(x=150, y=70)

    delete_button = tk.Button(delete_window, text="Delete", command=on_delete, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0, highlightbackground=border_color)
    delete_button.place(x=150, y=120)

    delete_window.mainloop()

def login():
    global username_entry, password_entry, connection, login_window

    username = username_entry.get()
    password = password_entry.get()

    connection = connect_to_database(username, password)
    if connection:
        login_window.destroy()  # Hide the login window

        root = tk.Tk()
        root.title("Inventory Management System")

        bg_image = Image.open("menu.jpg")
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        create_button = tk.Button(root, text="Create Item", command=create_item, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
        create_button.grid(row=0, column=0, padx=5, pady=5)

        read_button = tk.Button(root, text="Read Item", command=read_item, bg="#3498db", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
        read_button.grid(row=0, column=1, padx=5, pady=5)

        update_button = tk.Button(root, text="Update Item", command=update_item, bg="#f39c12", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
        update_button.grid(row=0, column=2, padx=5, pady=5)

        delete_button = tk.Button(root, text="Delete Item", command=delete_item, bg="#e74c3c", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
        delete_button.grid(row=0, column=3, padx=5, pady=5)

        root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def main():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login")

    bg_image = Image.open("menu.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    username_label = tk.Label(login_window, text="Username:", bg="#f0f0f0")
    username_label.place(relx=0.5, rely=0.4, anchor="center")
    username_entry = tk.Entry(login_window)
    username_entry.place(relx=0.6, rely=0.4, anchor="center")

    password_label = tk.Label(login_window, text="Password:", bg="#f0f0f0")
    password_label.place(relx=0.5, rely=0.5, anchor="center")
    password_entry = tk.Entry(login_window, show="*")
    password_entry.place(relx=0.6, rely=0.5, anchor="center")

    login_button = tk.Button(login_window, text="Login", command=login, bg="#2ecc71", fg="white", bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
    login_button.place(relx=0.5, rely=0.6, anchor="center")

    login_window.mainloop()

if __name__ == "__main__":
    main()
