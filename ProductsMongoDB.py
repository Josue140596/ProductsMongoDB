# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 01:38:34 2020

@author: Bryan 
"""

from tkinter import *
from tkinter import ttk
import pymongo 


client = pymongo.MongoClient("mongodb+srv://<cluster>:<pasword>@cluster.qkjgw.mongodb.net/ElecTienda?retryWrites=true&w=majority")

db = client.get_database('ElecTienda')
records = db.ElecTienda
        

class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Products App')
        
        
        
    #Crear un contenedor Frame
        frame = LabelFrame(self.wind, text = 'Register A new Project')
        frame.grid(row = 0, column = 0, columnspan= 3, pady = 20)
        
        #Name input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        
        #Price input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0 )
        self.price = Entry(frame)
        self.price.grid(row = 2, column= 1)
        
        #Button Add product
        ttk.Button(frame, text='Save product' , command = self.insert_Products  ).grid(row= 3, columnspan=2, sticky=(W, E))
        
        #Button Delete
        ttk.Button(text = 'Delete', command = self.delete_Products).grid(row = 5, column = 0, sticky=(W, E))
        #Button Edit
        ttk.Button(text = 'Edit', command = self.edit_or_update_Prodcust).grid(row = 5, column = 1, sticky=(W, E))
        #Table
        self.tree = ttk.Treeview(height=10, columns = 2)
        self.tree.grid(row= 4, column = 0, columnspan=2)
        self.tree.heading('#0', text = 'Name', anchor=CENTER, )
        self.tree.heading('#1', text = 'Price', anchor=CENTER)
        self.put_Products()
        
    def put_Products(self):
        
        self.tree.delete(*self.tree.get_children())
        self.name.delete(0, END)
        self.price.delete(0, END)
        pros = self.get_Products()
        for k in pros:
            self.tree.insert("", 1, text=k['name'], values=(k['price']))
            
      
       
        
    def get_Products(self):
        objects = list(records.find())
        
        return objects
    
    def insert_Products(self):
        
        namePro = self.name.get()
        pricePro = self.price.get()
        
        
        if(len(namePro) != 0 and len(pricePro) !=0):
            if( type(pricePro) == str ):
                menssage = self.message = Label(text='Put numbers in the price ' , fg= 'red')
                menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
                self.price.delete(0, END)
                self.price.focus()
           
                
            int(pricePro)
            new_Products = [{
            'name': namePro,
            'price': int(pricePro)
            }]
            records.insert_many(new_Products)
            self.tree.delete(*self.tree.get_children())
            self.put_Products()
            
            menssage = self.message = Label( fg= 'green')
            menssage['text'] = 'Product {} has been saved with the price {}'.format(namePro, pricePro)
            menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
            
        else:
            menssage = self.message = Label(text='Fill the inputs ' , fg= 'red')
            menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
        
        
    def delete_Products(self):
        try:
            
            selectItemName = self.tree.item(self.tree.selection())['text']
            selectItemPrice = self.tree.item(self.tree.selection())['values'][0]
           
            if(len(selectItemName) > 0):
                    records.delete_one({'name' : selectItemName})
                    menssage = self.message = Label( fg= 'green')
                    menssage['text'] = 'Product {} has been deleted '.format(selectItemName)
                    menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
                    self.put_Products()
            else:
                 menssage = self.message = Label(text= 'Select item ', fg= 'red')
                 menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
                    
    
        
            
        except IndexError as e:
            self.message['text'] = 'Please some item'
            
            return
        
        
    def edit_or_update_Prodcust(self):
        selectItemName = self.tree.item(self.tree.selection())['text']
        selectItemPrice = self.tree.item(self.tree.selection())['values'][0]
        
        if(len(selectItemName) > 0):
            
           
            menssage = self.message = Label( fg= 'green')
            menssage['text'] = 'Product {} editing '.format(selectItemName)
            menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
            
            self.put_Products()
        else:
            menssage = self.message = Label(text= 'Select item ', fg= 'red')
            menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
        
        #Nueva Ventana
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edith or Update Products'
        
        #Crear un contenedor Frame
        frame_wind = LabelFrame(self.edit_wind, text = 'Edit or update Product')
        frame_wind.grid(row = 0, column = 0, columnspan= 3, pady = 20)
        
        #Name input
        Label(frame_wind, text = 'Name: ').grid(row = 1, column = 0)
        self.name_wind = Entry(frame_wind)
        self.name_wind.focus()
        self.name_wind.grid(row = 1, column = 1)
        
        #Price input
        Label(frame_wind, text = 'Price: ').grid(row = 2, column = 0 )
        self.price_wind = Entry(frame_wind)
        self.price_wind.grid(row = 2, column= 1)
        
        
        
        def get_edit_products():
            
            nameWind = self.name_wind.get()
            priceWind = self.price_wind.get()
            
           
            
            print(priceWind)
           #update data 
            if(len(nameWind) > 0 and len(priceWind) > 0 ):
                records.update_one({'name':selectItemName}, {'$set':{ 'name': nameWind, 'price': int(priceWind)}})
                menssage = self.message = Label( fg= 'green')
                menssage['text'] = 'Product {} has been modidfy '.format(selectItemName)
                menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
                self.edit_wind.destroy()
            
            else:
                menssage = self.message = Label( frame_wind, fg= 'Red')
                menssage['text'] = 'Product hasn''t been modidfy fill the inputs '
                menssage.grid(row = 3, column=0, columnspan=2, sticky=(W, E))
                
            
            self.put_Products()
            
        #Button Save
        ttk.Button(frame_wind, text = 'Save', command = get_edit_products).grid(row = 5, column = 1, sticky=(W, E))
            
if __name__ == '__main__':  
    window = Tk()
    app = Product(window)
    
    window.mainloop()
    