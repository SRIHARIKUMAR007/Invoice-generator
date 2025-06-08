import tkinter as tk
from tkinter import messagebox, ttk, font
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import datetime

# MySQL database configuration
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'hello'
MYSQL_DATABASE = 'hello'

class InvoiceManagementSystem:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.create_widgets()

    def setup_main_window(self):
        self.root.title("🧾 Invoice Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Custom fonts
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.label_font = font.Font(family="Arial", size=10, weight="bold")
        self.button_font = font.Font(family="Arial", size=10, weight="bold")

    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title with icon
        title_frame = tk.Frame(main_frame, bg='#f0f0f0')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="📊 Invoice Management System", 
                              font=self.title_font, bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Tab 1: Add Invoice
        self.create_add_invoice_tab()
        
        # Tab 2: Generate PDFs
        self.create_pdf_tab()
        
        # Tab 3: View Invoices
        self.create_view_tab()

        # Status bar
        self.create_status_bar(main_frame)

    def create_add_invoice_tab(self):
        # Add Invoice Tab
        add_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(add_frame, text="➕ Add Invoice")

        # Form container with border
        form_frame = tk.LabelFrame(add_frame, text="📝 Invoice Details", 
                                  font=self.label_font, bg='white', fg='#34495e',
                                  padx=20, pady=20, relief=tk.GROOVE, bd=2)
        form_frame.pack(fill=tk.X, pady=20)

        # Input fields with enhanced styling
        fields = [
            ("👤 Customer ID:", "customer_id"),
            ("📛 Customer Name:", "customer_name"), 
            ("📦 Item Name:", "item_name"),
            ("🔢 Quantity:", "quantity"),
            ("💰 Price ($):", "price")
        ]

        self.entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            label = tk.Label(form_frame, text=label_text, font=self.label_font, 
                           bg='white', fg='#2c3e50', anchor='w')
            label.grid(row=i, column=0, sticky='w', padx=(0, 10), pady=8)
            
            # Entry with styling
            entry = tk.Entry(form_frame, font=('Arial', 10), width=25, 
                           relief=tk.FLAT, bd=5, bg='#ecf0f1')
            entry.grid(row=i, column=1, sticky='ew', pady=8)
            entry.bind('<FocusIn>', lambda e: e.widget.config(bg='#d5dbdb'))
            entry.bind('<FocusOut>', lambda e: e.widget.config(bg='#ecf0f1'))
            
            self.entries[field_name] = entry

        form_frame.columnconfigure(1, weight=1)

        # Buttons frame
        button_frame = tk.Frame(add_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)

        # Add Invoice Button
        add_btn = tk.Button(button_frame, text="💾 Add Invoice", 
                           command=self.insert_invoice,
                           font=self.button_font, bg='#27ae60', fg='white',
                           relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        add_btn.bind('<Enter>', lambda e: e.widget.config(bg='#2ecc71'))
        add_btn.bind('<Leave>', lambda e: e.widget.config(bg='#27ae60'))

        # Clear Button
        clear_btn = tk.Button(button_frame, text="🗑️ Clear Fields", 
                             command=self.clear_fields,
                             font=self.button_font, bg='#f39c12', fg='white',
                             relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        clear_btn.pack(side=tk.LEFT)
        clear_btn.bind('<Enter>', lambda e: e.widget.config(bg='#e67e22'))
        clear_btn.bind('<Leave>', lambda e: e.widget.config(bg='#f39c12'))

    def create_pdf_tab(self):
        # Generate PDF Tab
        pdf_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(pdf_frame, text="📄 Generate PDF")

        # PDF Generation container
        pdf_container = tk.LabelFrame(pdf_frame, text="🖨️ PDF Generation", 
                                     font=self.label_font, bg='white', fg='#34495e',
                                     padx=20, pady=20, relief=tk.GROOVE, bd=2)
        pdf_container.pack(fill=tk.X, pady=20)

        # Customer ID for PDF
        tk.Label(pdf_container, text="👤 Customer ID:", font=self.label_font, 
                bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=10)
        
        self.pdf_customer_id = tk.Entry(pdf_container, font=('Arial', 10), width=25,
                                       relief=tk.FLAT, bd=5, bg='#ecf0f1')
        self.pdf_customer_id.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=10)
        self.pdf_customer_id.bind('<FocusIn>', lambda e: e.widget.config(bg='#d5dbdb'))
        self.pdf_customer_id.bind('<FocusOut>', lambda e: e.widget.config(bg='#ecf0f1'))

        pdf_container.columnconfigure(1, weight=1)

        # Generate PDF Button
        pdf_btn = tk.Button(pdf_container, text="📄 Generate PDFs", 
                           command=self.generate_pdf,
                           font=self.button_font, bg='#3498db', fg='white',
                           relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        pdf_btn.grid(row=1, column=0, columnspan=2, pady=20)
        pdf_btn.bind('<Enter>', lambda e: e.widget.config(bg='#2980b9'))
        pdf_btn.bind('<Leave>', lambda e: e.widget.config(bg='#3498db'))

    def create_view_tab(self):
        # View Invoices Tab
        view_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(view_frame, text="👁️ View Invoices")

        # Search frame
        search_frame = tk.LabelFrame(view_frame, text="🔍 Search Invoices", 
                                    font=self.label_font, bg='white', fg='#34495e',
                                    padx=20, pady=20, relief=tk.GROOVE, bd=2)
        search_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(search_frame, text="👤 Customer ID (optional):", 
                font=self.label_font, bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w')
        
        self.search_customer_id = tk.Entry(search_frame, font=('Arial', 10), width=20,
                                          relief=tk.FLAT, bd=5, bg='#ecf0f1')
        self.search_customer_id.grid(row=0, column=1, padx=(10, 0), sticky='w')

        search_btn = tk.Button(search_frame, text="🔍 Search", 
                              command=self.view_invoices,
                              font=self.button_font, bg='#9b59b6', fg='white',
                              relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        search_btn.grid(row=0, column=2, padx=(10, 0))
        search_btn.bind('<Enter>', lambda e: e.widget.config(bg='#8e44ad'))
        search_btn.bind('<Leave>', lambda e: e.widget.config(bg='#9b59b6'))

        # Treeview for displaying invoices
        tree_frame = tk.Frame(view_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('ID', 'Customer ID', 'Customer Name', 'Item', 'Quantity', 'Price', 'Total')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_status_bar(self, parent):
        self.status_bar = tk.Label(parent, text="Ready", relief=tk.SUNKEN, 
                                  anchor=tk.W, bg='#34495e', fg='white', 
                                  font=('Arial', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def update_status(self, message):
        self.status_bar.config(text=f"Status: {message}")
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.update_status("Fields cleared")

    def insert_invoice(self):
        customer_id = self.entries['customer_id'].get()
        customer_name = self.entries['customer_name'].get()
        item_name = self.entries['item_name'].get()
        quantity = self.entries['quantity'].get()
        price = self.entries['price'].get()
        
        if not all([customer_id, customer_name, item_name, quantity, price]):
            messagebox.showerror("❌ Error", "Please fill in all fields")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
            customer_id = int(customer_id)
        except ValueError:
            messagebox.showerror("❌ Error", "Customer ID, quantity, and price must be numbers")
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
            messagebox.showinfo("✅ Success", "Invoice details inserted successfully")
            self.clear_fields()
            self.update_status("Invoice added successfully")
        except mysql.connector.Error as e:
            messagebox.showerror("❌ Error", f"Error inserting invoice details: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def generate_pdf(self):
        customer_id = self.pdf_customer_id.get()
        if not customer_id:
            messagebox.showerror("❌ Error", "Please enter a customer ID to generate PDFs")
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
                messagebox.showinfo("ℹ️ Info", "No invoices found for the specified customer")
                return

            for invoice in invoices:
                if len(invoice) >= 7:
                    pdf_file = f"Invoice_{invoice[0]}_{invoice[2].replace(' ', '_')}.pdf"
                    c = canvas.Canvas(pdf_file, pagesize=letter)
                    
                    # Enhanced PDF with colors and better formatting
                    c.setFillColor(HexColor('#2c3e50'))
                    c.setFont("Helvetica-Bold", 18)
                    c.drawString(100, 750, "INVOICE")
                    
                    # Date
                    c.setFont("Helvetica", 10)
                    c.drawString(450, 750, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
                    
                    # Line separator
                    c.setStrokeColor(HexColor('#3498db'))
                    c.line(100, 735, 500, 735)
                    
                    # Invoice details with better formatting
                    c.setFillColor(HexColor('#34495e'))
                    c.setFont("Helvetica-Bold", 12)
                    
                    y_pos = 700
                    details = [
                        f"Invoice ID: {invoice[0]}",
                        f"Customer ID: {invoice[1]}",
                        f"Customer Name: {invoice[2]}",
                        f"Item: {invoice[3]}",
                        f"Quantity: {invoice[4]}",
                        f"Unit Price: ${invoice[5]:.2f}",
                        f"Total Amount: ${invoice[6]:.2f}"
                    ]
                    
                    for detail in details:
                        c.drawString(100, y_pos, detail)
                        y_pos -= 25
                    
                    # Footer
                    c.setFont("Helvetica-Oblique", 8)
                    c.setFillColor(HexColor('#7f8c8d'))
                    c.drawString(100, 100, "Generated by Invoice Management System")
                    
                    c.save()
                else:
                    messagebox.showerror("❌ Error", f"Unexpected format in fetched invoice data: {invoice}")
            
            messagebox.showinfo("✅ Success", f"PDFs generated successfully for Customer ID: {customer_id}")
            self.update_status(f"PDFs generated for Customer {customer_id}")
        except mysql.connector.Error as e:
            messagebox.showerror("❌ Error", f"Error generating PDFs: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def view_invoices(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        customer_id = self.search_customer_id.get()
        
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            cursor = conn.cursor()

            if customer_id:
                select_query = "SELECT * FROM invoices WHERE customer_id = %s"
                cursor.execute(select_query, (customer_id,))
            else:
                select_query = "SELECT * FROM invoices"
                cursor.execute(select_query)
            
            invoices = cursor.fetchall()
            
            for invoice in invoices:
                self.tree.insert('', tk.END, values=invoice)
            
            self.update_status(f"Loaded {len(invoices)} invoices")
            
        except mysql.connector.Error as e:
            messagebox.showerror("❌ Error", f"Error fetching invoices: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceManagementSystem(root)
    root.mainloop()
