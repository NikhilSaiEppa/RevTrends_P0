import os
x='Hell.txt'
if os.path.exists(x):
    file=open('Hello.txt','r')
    c=file.read()
    print(c)
else:
    print("File name is not find")


# file=open('Hellos.txt','r')





