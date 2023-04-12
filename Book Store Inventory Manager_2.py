#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import csv module to work with csv files and ABC class from abc module for abstract classes
import csv
from abc import ABC, abstractmethod


# Create an abstract class named Item to serve as a base class for books and magazines
class Item(ABC):
    def __init__(self, title, author, price, stock):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    @abstractmethod
    def item_type(self):
        pass

    def __str__(self):
        return f"{self.title} by {self.author}: ${self.price} ({self.stock} in stock)"


# Create a Book class that inherits from Item
class Book(Item):
    def item_type(self):
        return "Book"


# Create a Magazine class that inherits from Item

class Magazine(Item):
    def item_type(self):
        return "Magazine"


# Create a Bookstore class to manage the store's inventory and operations


class BookStore:
    def __init__(self, file_name):
        self.file_name = file_name
        self.items = []
        self.load_items()  # call load_items method to read the data from file_name

    def load_items(self):
        try:
            with open(self.file_name, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # skip header row

                for row in reader:
                    # extract the values from the row
                    title, author, price, stock, item_type = row
                    price = int(price)
                    stock = int(stock)
                    # create a new item object based on the item_type
                    if item_type == "Book":
                        item = Book(title, author, price, stock)
                    else:
                        item = Magazine(title, author, price, stock)
                    self.items.append(item)  # add item to the items list

        except FileNotFoundError:
            pass

    def save_items(self):
        # write the items data to the file
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'Price', 'Stock', 'Type'])
            for item in self.items:
                writer.writerow([item.title, item.author, item.price, item.stock, item.item_type()])

    def add_item(self, item):
        self.items.append(item)
        self.save_items()  # call save_items method to save the new item to the file

        print(f"{item.item_type()} added successfully.")

    def sell_item(self, title):
        found = False
        for item in self.items:
            if item.title == title:
                found = True
                print(item)
                while True:
                    choice = input("Do you want to sale this item? (y/n) ").lower()
                    if choice == 'y':
                        item.stock -= 1
                        if item.stock == 0:
                            self.items.remove(item)
                        self.save_items()  # update the stock and save the changes to the file

                        print(f"{item.item_type()} sold successfully.")
                        break
                    elif choice == 'n':
                        print("Sale cancelled.")
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                break
        if not found:
            print("Item not available.")

    # search item in the csv file
    def search_item(self, title):
        found = False
        for item in self.items:
            if item.title == title:
                found = True
                print(item)
                break
        if not found:
            print("Item not available.")

    # Display Menu
    def display_menu(self):
        print("Welcome to the Store!")
        while True:
            print("\nSelect an option:")
            print("1. Add new item")
            print("2. Sell item")
            print("3. Search item")
            print("4. Exit")
            choice = input("Enter choice (1-4): ")
            if choice == '1':
                title = input("Enter item title: ")
                author = input("Enter author/publisher name: ")
                while True:
                    try:
                        price = int(input("Enter item price: "))
                        break
                    except ValueError:
                        print("Please enter a valid integer price.")
                while True:
                    try:
                        stock = int(input("Enter item stock: "))
                        break
                    except ValueError:
                        print("Please enter a valid integer stock.")
                while True:
                    item_type = input("Enter item type (Book/Magazine): ")
                    if item_type == "Book":
                        item = Book(title, author, price, stock)
                        break
                    elif item_type == "Magazine":
                        item = Magazine(title, author, price, stock)
                        break
                    else:
                        print("Please enter a valid item type.")
                self.add_item(item)
            elif choice == '2':
                title = input("Enter item title to sell: ")
                self.sell_item(title)
            elif choice == '3':
                title = input("Enter item title to search: ")
                self.search_item(title)
            elif choice == '4':
                break
            else:
                print("Please enter a valid choice (1-4)")


# Main
if __name__ == '__main__':
    store = BookStore('items.csv')
    store.display_menu()


# In[ ]:




