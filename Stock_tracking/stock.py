import tkinter as tk 
from tkinter import ttk
import sqlite3 



class StockTrackingApp:
    def __init__(self,root):
      # Create Main Window 
      self.root = root 
      self.root.title("İstanbul Çiçek Ve Ambalaj Malzemeleri Stok Takip")

       # Create Data Base 
       # Create Necessary Table

      self.conn = sqlite3.connect("StockTracking.db")
      self.cursor = self.conn.cursor()
      self.cursor.execute ("""
             CREATE TABLE IF NOT EXISTS stock(
                         id TEXT PRIMARY KEY,
                         product_name TEXT,
                         piece INTEGER ,
                         unit_price REAL ,
                         total_value REAL
                    )                                                                                 
             """)
    
      self.conn.commit()
      # Login Areas
      self.id_label = tk.Label(root,text= "ID:")
      self.id_label.grid(row = 0,column= 0)
      self.id_entry = tk.Entry(root)
      self.id_entry.grid(row = 0,column = 1)

      # Product Name Label and Login Box 
      self.product_name_label = tk.Label(root,text="Ürün Adı :")
      self.product_name_label.grid(row = 1,column= 0 )
      self.product_name_entry = tk.Entry(root)
      self.product_name_entry.grid(row =1 , column =1)

      # Piece Name Label and Login Box
      self.piece_name_label = tk.Label(root,text="Adet:")
      self.piece_name_label.grid(row=2,column=0)
      self.piece_name_entry = tk.Entry(root)
      self.piece_name_entry.grid(row = 2,column = 1)

      # Unit Label and Login Box 
      self.unit_label =tk.Label(root,text ="Birim Fiyatı :" )
      self.unit_label.grid(row=3,column=0)
      self.unit_entry = tk.Entry(root)
      self.unit_entry.grid(row=3,column=1)
    
      # Process button
      self.add_button = tk.Button(root,text="Ekle",command=self.add)
      self.add_button.grid(row=4, column=0, columnspan= 1)

      # Correction(Fix it)
      self.fix_button = tk.Button (root,text ="Düzelt ",command=self.fix)
      self.fix_button.grid(row=4,column=1,columnspan = 1 )

      # Delete
      self.delete_button=tk.Button(root,text="Sil",command=self.delete)
      self.delete_button.grid(row=4,column=2,columnspan=1)

      # Clean Button
      self.clean_button =tk.Button (root,text="Temizle",command=self.clear)
      self.clean_button.grid(row=4,column=3,columnspan=1)

      # Search Bar
      self.search_label = tk.Label(root,text = "Ara :")
      self.search_label.grid(row = 5 , column= 0)
      self.search_entry = tk.Entry(root)
      self.search_entry.grid(row =5,column =1 )

      # Search Trigger
      self.search_entry.bind("<KeyRelease>",self.search)

      # Create Table
      self.table = ttk.Treeview(root, columns =("ID","Product Name","Piece","Unit Price","Total Value"),show="headings" )
      self.table.heading("ID",text="ID")
      self.table.heading("Product Name",text="Ürün Adı")
      self.table.heading("Piece",text="Adet")
      self.table.heading("Unit Price",text="Birim Fiyat")
      self.table.heading("Total Value",text="Toplam Değer")
      self.table.grid(row=6,column=0,columnspan=4)
 
      # Data Processing Starts When The Table is Clicked
      self.table.bind("<ButtonRelease-1>", self.select_row)
     
      # Loading Old Data
      self.loading_old_data()

      # Main Function Finish
    def add(self):
        id = self.id_entry.get()
        product_name = self.product_name_entry.get()
        piece = int(self.piece_name_entry.get())
        unit_price= float (self.unit_entry.get())
        total_value = str(piece * unit_price) +" TL"

        self.cursor.execute("INSERT INTO stock VALUES (?,?,?,?,?)", (id,product_name,piece,unit_price,total_value) )
        self.conn.commit()

        self.table.insert("","end",values=(id,product_name,piece,unit_price,total_value))
        self.clear() 
    def clear(self):
        self.id_entry.delete(0,tk.END)
        self.product_name_entry.delete(0,tk.END)
        self.piece_name_entry.delete(0,tk.END)
        self.unit_entry.delete(0,tk.END)
    def search(self,event):
         search_text = self.search_entry.get().lower()
         for item in self.table.get_children():
             values = self.table.item(item,"values")
             if search_text in values[0].lower() or search_text in values [1].lower() or search_text in values [2].lower() or search_text in values [3].lower() :
                self.table.selection_set(item)
                self.table.see(item)
             else :
                 self.table.selection_remove(item)
    def select_row(self,event):
        
        select = self.table.selection()
        if select :
             item = self.table.item(select)
             values = item["values"]
             self.id_entry.delete(0,tk.END)
             self.id_entry.insert(0,values[0])
             self.product_name_entry.delete(0,tk.END)
             self.product_name_entry.insert(0,values[1])
             self.piece_name_entry.delete(0,tk.END)
             self.piece_name_entry.insert(0,values[2])
             self.unit_entry.delete(0,tk.END)
             self.unit_entry.insert(0,values[3])
    def fix(self):
        select = self.table.selection()
        if select :
            
              id = self.id_entry.get()
              product_name = self.product_name_entry.get()
              piece = int(self.piece_name_entry.get())
              unit_price= float (self.unit_entry.get())
              total_value = piece * unit_price 
        
              self.cursor.execute("UPDATE stock SET product_name = ? ,piece = ?, unit_price = ?, total_value = ? WHERE id=?" , ( product_name,piece, unit_price,total_value, id) )
              self.table.item(select , values= (id,product_name,piece,unit_price,total_value))
              self.clear()
    def delete (self):
        select = self.table.selection()
        if select:
            id = self.table.item(select)['values'][0]
            self.cursor.execute("DELETE FROM stock WHERE id = ?",(id,))
            self.conn.commit()
            self.table.delete(select)
            self.clear() 
    def  loading_old_data(self):
            for row in self.cursor.execute("SELECT *FROM stock"):
                self.table.insert("","end",values = row)

        
if __name__ == "__main__":
    root=tk.Tk()
    app=StockTrackingApp(root)
    root.mainloop()      

                     

      




     

     
      









      

