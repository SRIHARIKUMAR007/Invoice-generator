import tkinter as tk
from tkinter import messagebox
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# MySQL database configuration
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'hello'
MYSQL_DATABASE = 'raj'

def insert_invoice():
    customer_id = customer_id_entry.get()
    customer_name = customer_name_entry.get()
    item_name = item_name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    
    if not all([customer_id, customer_name, item_name, quantity, price]):
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    try:
        quantity = int(quantity)
        price = float(price)
        customer_id = int(customer_id)
    except ValueError:
        messagebox.showerror("Error", "Customer ID, quantity, and price must be numbers")
        return
    
    total_amount = quantity * price

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO invoices (customer_id, customer_name, item_name, quantity, price, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (customer_id, customer_name, item_name, quantity, price, total_amount))
        conn.commit()
        messagebox.showinfo("Success", "Invoice details inserted successfully")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error inserting invoice details: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def generate_pdf():
    customer_id = customer_id_entry.get()
    if not customer_id:
        messagebox.showerror("Error", "Please enter a customer ID to generate PDFs")
        return
    
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        select_query = "SELECT * FROM invoices WHERE customer_id = %s"
        cursor.execute(select_query, (customer_id,))
        invoices = cursor.fetchall()
        
        if not invoices:
            messagebox.showinfo("Info", "No invoices found for the specified customer")
            return

        for invoice in invoices:
            pdf_file = f"{invoice[0]}_{invoice[2]}_invoice.pdf"  # Using invoice ID and item name for filename
            c = canvas.Canvas(pdf_file, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, f"Customer ID: {invoice[1]}")
            c.drawString(100, 730, f"Customer Name: {invoice[2]}")
            c.drawString(100, 710, f"Item: {invoice[3]}")
            c.drawString(100, 690, f"Quantity: {invoice[4]}")
            c.drawString(100, 670, f"Price: ${invoice[5]}")
            c.drawString(100, 650, f"Total Amount: ${invoice[6]}")
            c.save()
        
        messagebox.showinfo("Success", "PDFs generated successfully")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error generating PDFs: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Create GUI
root = tk.Tk()
root.title("Invoice Management System")

tk.Label(root, text="Customer ID:").grid(row=0, column=0)
customer_id_entry = tk.Entry(root)
customer_id_entry.grid(row=0, column=1)

tk.Label(root, text="Customer Name:").grid(row=1, column=0)
customer_name_entry = tk.Entry(root)
customer_name_entry.grid(row=1, column=1)

tk.Label(root, text="Item Name:").grid(row=2, column=0)
item_name_entry = tk.Entry(root)
item_name_entry.grid(row=2, column=1)

tk.Label(root, text="Quantity:").grid(row=3, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=3, column=1)

tk.Label(root, text="Price:").grid(row=4, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1)

insert_invoice_button = tk.Button(root, text="Insert Invoice", command=insert_invoice)
insert_invoice_button.grid(row=5, column=0, columnspan=2)

generate_pdf_button = tk.Button(root, text="Generate PDFs", command=generate_pdf)
generate_pdf_button.grid(row=6, column=0, columnspan=2)

root.mainloop()
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# MySQL database configuration
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'hello'
MYSQL_DATABASE = 'hello'

def generate_pdf():
    customer_id = customer_id_entry.get()
    if not customer_id:
        messagebox.showerror("Error", "Please enter a customer ID to generate PDFs")
        return
    
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        select_query = "SELECT * FROM invoices WHERE customer_id = %s"
        cursor.execute(select_query, (customer_id,))
        invoices = cursor.fetchall()
        
        if not invoices:
            messagebox.showinfo("Info", "No invoices found for the specified customer")
            return

        for invoice in invoices:
            if len(invoice) >= 7:  # Check if the tuple has at least 7 elements
                pdf_file = f"{invoice[0]}_{invoice[2]}_invoice.pdf"  # Using invoice ID and item name for filename
                c = canvas.Canvas(pdf_file, pagesize=letter)
                c.setFont("Helvetica", 12)
                c.drawString(100, 750, f"Customer ID: {invoice[1]}")
                c.drawString(100, 730, f"Customer Name: {invoice[2]}")
                c.drawString(100, 710, f"Item: {invoice[3]}")
                c.drawString(100, 690, f"Quantity: {invoice[4]}")
                c.drawString(100, 670, f"Price: ${invoice[5]}")
                c.drawString(100, 650, f"Total Amount: ${invoice[6]}")
                c.save()
            else:
                messagebox.showerror("Error", f"Unexpected format in fetched invoice data: {invoice}")
        
        messagebox.showinfo("Success", "PDFs generated successfully")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error generating PDFs: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Create GUI
root = tk.Tk()
root.title("Generate PDFs for Customer")

tk.Label(root, text="Customer ID:").grid(row=0, column=0)
customer_id_entry = tk.Entry(root)
customer_id_entry.grid(row=0, column=1)

generate_pdf_button = tk.Button(root, text="Generate PDFs", command=generate_pdf)
generate_pdf_button.grid(row=1, column=0, columnspan=2)

root.mainloop()
