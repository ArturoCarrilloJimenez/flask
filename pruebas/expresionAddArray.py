list = ['pepe','juana','carlos','sofia'];

newList = [x for x in list if 'a' in x];

"""
Es lo mismo que la expresion de arriba

for i in list :
    if 'a' in i:
        newList.append(i); 
"""

print(newList);