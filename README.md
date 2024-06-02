# Inventory Management System README

---

Welcome to the Inventory Management System project! This README provides a detailed guide on how to set up and use the system, including the creation of the database, tables, and a walkthrough of the Python code. Let's get started! 🎉

---


### Features

- **User Authentication:** Secure login using MySQL authentication.
- **Create Item:** Add new items to the inventory with details like name, description, quantity, and price.
- **Read Item:** Search and display item details based on Item ID or Name.
- **Update Item:** Update the quantity of items in the inventory.
- **Delete Item:** Remove items from the inventory after confirmation.

---

### Getting Started

#### Prerequisites

Ensure you have the following installed on your system:
- Python 3.x
- MySQL
- pip (Python package installer)

#### Database Setup

1. **Create the Database:**
   ```sql
   CREATE DATABASE inventory_management;
   USE inventory_management;

2. **Create the "items" Table:**
    ```sql
    CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(255),
    quantity INT,
    price DECIMAL(10,2)
    );

3. **Insert Sample Data:**
    ```sql
    INSERT INTO items (name, description, quantity, price) VALUES 
    ('Laptop', 'Dell XPS 13', 1000, 1200.00),
    ('Monitor', 'Dell 27-inch IPS Monitor', 800, 300.00),
    ('Keyboard', 'Logitech Wireless Keyboard', 1500, 50.00),
    ('Mouse', 'Logitech Gaming Mouse', 2000, 40.00),
    ('Headphones', 'Sony Noise Cancelling', 1200, 150.00),
    ('Smartphone', 'Samsung Galaxy S20', 500, 900.00),
    ('Tablet', 'Apple iPad Pro', 700, 800.00);

4. **Create MySQL Users and Grant Privileges:**
   ```sql
   CREATE USER 'user1'@'localhost' IDENTIFIED BY 'user123';
    CREATE USER 'user2'@'localhost' IDENTIFIED BY 'user456';
    CREATE USER 'user3'@'localhost' IDENTIFIED BY 'user789';
    GRANT ALL ON inventory_management.* TO 'user1'@'localhost';
    GRANT ALL ON inventory_management.* TO 'user2'@'localhost';
    GRANT ALL ON inventory_management.* TO 'user3'@'localhost';
    FLUSH PRIVILEGES;
---
## Project Setup

1. Clone the repository
2. Install required dependencies
   ```python
   pip install mysql-connector-python pillow
3. Run the application
   ```python
   python inventory_management_system.py
---
## Python Code Walkthrough

**Database Connection**

The function **"connect_to_database"** establishes a connection to the MySQL database using the provided username and password.

  ```python
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
```


**Create Item**

The **"create_item"** function creates a new item in the database. It collects item details from the user and inserts them into the **items** table.

```python
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

    # need to place UI code here...

    create_window.mainloop()
```

**Read Item**

The **"read_item"** function allows users to search for an item by its ID or name and displays its details.

```python
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

    # need to write UI code here...

    read_window.mainloop()
```
**Update Item**

The **"update_item"** function updates the quantity of an item in the inventory.

```python
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

    # need to write UI code here...

    update_window.mainloop()
```
**Delete Item**

The **"delete_item"** function deletes an item from the inventory.

```python
def delete_item():
    global connection, delete_window

    def on_delete():
        item_id = item_id_entry.get()

        try:
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            connection.commit()
            messagebox.showinfo("Success", "Item deleted successfully")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error deleting item: {e}")

        delete_window.destroy()

    # need to place UI code here...

    delete_window.mainloop()
```

---

## User Interface Overview
**Login Screen**
The initial login screen where users enter their credentials.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/2dc7a560-6be1-482c-897a-48f750a879ab)


**Main Menu**
The main menu with options to create, read, update, and delete items.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/57882631-fabe-4055-8a4b-bee858cff24c)


**Create Item Screen**
The form where users can add new items to the inventory.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/417e6f67-3ae4-401b-b48f-88ae8bf3653c)


**Read Item Screen**
The search functionality and display of item details.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/b942e419-880a-470e-a38c-38c27f03b4e6)


**Update Item Screen**
The form used to update the quantity of items in the inventory.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/ec99c9ba-9ece-4efa-b3b4-b62ca475c047)


**Delete Item Screen**
The confirmation screen for item deletion.

![image](https://github.com/harimoram/Inventory_Management_System/assets/93645511/3dbe8722-48d7-4435-af93-3847cb165f29)


---

## Future Enhancements

- **User Role Management:** Implement roles and permissions.

- **Enhanced Security:** Add password encryption.

- **Reporting:** Generate inventory reports.

- **User Interface Improvements:** Improve the GUI design for a better user experience.

---

By following this detailed guide, you should be able to set up and use the Inventory Management System successfully. Happy coding! 🚀








