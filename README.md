# Problem Definition
## SQL is hard
Changing data structures is hard. Tables, INSERTS, UPDATES, SELECTS, and DELETES all have to be updated when a new attribute is added.  
## But it doesn't have to be
All of these could be fixed if metaprogramming was utilized. Preferably, there should be one master file, from which all definitions should come.
Optimally, this would be a class file, and then the class would just conform to a certain protocol and all necessary methods would be available. \
Problem: this will not work for all implementations. However, the goal will be to make it as general as possible.
# EasySQL
