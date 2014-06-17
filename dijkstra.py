__author__ = 'Зидерер Антон'

#импорт библиотек
from tkinter import *
import itertools
from random import randrange


#Значения по умолчанию
#массив с вершинами
vert_array = []
#массив с связями
link_array = []


#текущий шаг 
step = 0
  
#класс для вершин графа 
class Vertex():
    cost = 9999
    hold = 0
    x = 0
    y = 0
  
    def __init__(self,cost = 9999, x = 0, y = 0):
        self.cost = cost
        self.x = x
        self.y = y
  
#класс для свойств и методов связей 
class Link(): 
    begin = 0
    end = 0
    length = 0
  
    def __init__(self,begin,end,length): 
        self.begin = begin 
        self.end = end 
        self.length = length 
  

#отрисовка линий
def reset():
    global canv,link_array

    #очистка массива со связями
    link_array = []

    #очистка холста от линий и надписей
    canv.delete("lines")
    canv.delete("labels")

    #генерация линий
    for i in itertools.combinations('012345',2):
        if randrange(0,2):
            linkcost = randrange(1,10)
            if linkcost > 5:
                sm = 20
            else:
                sm = -20
            canv.create_line(vert_array[int(i[0])].x,vert_array[int(i[0])].y,vert_array[int(i[1])].x,vert_array[int(i[1])].y,width=2,tag="lines")
            canv.create_text((((vert_array[int(i[0])].x+vert_array[int(i[1])].x)/2+5)),((vert_array[int(i[0])].y+vert_array[int(i[1])].y)/2 + sm),text=str(linkcost),fill="green",font="Arial 14",tag="labels")
            link = Link(vert_array[int(i[0])],vert_array[int(i[0])],linkcost)
            link_array.append(link)
        print(i)

    for item in vert_array:
        #обнуление стоимости всех вершин
        item.cost = 9999
        canv.create_oval(item.x-15, item.y-15, item.x+15, item.y+15, fill="white", outline="black", width = 2, tag="vertex")



def vibor():
    pass
    
def click(e): 

    status = 0
    for item in vert_array:
        if item.cost == 0:
            status = 1

    if status == 0:
        for item in vert_array:
            if item.x >= e.x - 15 and item.x <= e.x + 15 and item.y >= e.y - 15 and item.y <= e.y + 15:
                item.cost = 0
                canv.create_oval(item.x-15, item.y-15, item.x+15, item.y+15, fill="green", outline="black", width = 2, tag="vertex")
                break

#создание окна для размещения вершин графа 
root = Tk() 
root.geometry("450x450+350+150") 
root.title("Dijkstra algorithm") 
  
#холст для вершин графа
canv = Canvas(root, width = 450,height = 380, bg = "white") 
canv.pack()

#создание вершины
y = 20
for i in range(3):
    x = 10
    for j in range(4):
        if ((i == 0 or i == 2) and (j == 1 or j == 2)) or (i == 1 and (j == 0 or j == 3)):
            #canv.create_oval(x+5, y+5, x+35, y+35, fill="white", outline="black", width = 2, tag="vertex")
            obj = Vertex(9999,x+15,y+15)
            vert_array.append(obj)
        x += 135
    y += 160

print(vert_array)

#Добавление надписи

lbl = Label(root) 
lbl["text"] = "Шаг1. Выберите стартовую точку"
lbl.pack() 

#Добавление кнопки для отрисовки линий между вершинами
btn1 = Button(root) 
btn1["command"] = reset 
btn1["text"] = "Заново"
btn1.pack() 


#добавить слушателя на клик мыши 
root.bind("<Button-1>", click)

root.mainloop()
