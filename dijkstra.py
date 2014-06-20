__author__ = 'Александр Кудрявцев'

#импорт библиотек
from tkinter import *
import itertools
import math
from random import randrange
from vertices_and_links import *
from tkinter.messagebox import *

#Значения по умолчанию
#массив с вершинами
vert_array = []
#массив с связями
link_array = []
#количество вершин
vert_count = 10
#идентификатор текстового поля для установления количества вершин
count_ent = 0
#текущий шаг
step = 0
win1 = 0

#функция отображения информации о программе
def about():
    showinfo("Информация","Визуализатор алгоритма Дейкстры\nВсе права защищены\n2014 год")

def settings_change():
    global vert_count
    vert_count = int(count_ent.get())
    if not(vert_count < 10 and vert_count > 0):
        showinfo("Ошибка","Количество вершин не должно превышать 10 и быть меньше 0")
    else:
        win1.destroy()

#изменение настроек приложения
def settings():
    global win1,count_ent
    win1 = Toplevel()
    #win1.configure("100x100")
    Label(win1, text="Введите количество вершин").grid(row=0,column=0,sticky=W,columnspan=2)
    count_ent = Entry(win1, width=5)
    count_ent.grid(row=1, column=0)
    Button(win1, text="Установить", command=settings_change).grid(row=1, column=1)


#отрисовка линий между вершинами
def reset():
    global canv, link_array,vert_array,vert_count

    #порядковый номер вершины для обращения к ней по тегу
    vert_number = 0

    #удалить овалы
    for item in vert_array:
        #удалить метки со стоимостью перехода
        canv.delete("vert"+str(item.number))

    #обнулить массив с вершинами
    vert_array = []

    #создание вершины
    #найти координаты точек, где будут находится центры вершин
    #поделить 360 градусов на количество вершин - это шаг угла (в градусах)
    vert_grad = 360 // vert_count
    for grad in range(0, 360, vert_grad):
        x = math.cos(grad*(math.pi/180))*200 + 300
        y = math.sin(grad*(math.pi/180))*200 + 250
        obj = Vertex(9999,x+15,y+15,vert_number)
        vert_array.append(obj)
        vert_number += 1

    #очистка массива со связями
    link_array = []

    #очистка холста от линий и надписей
    canv.delete("lines")
    canv.delete("labels")

    #сгенерировать строку из номеров всех вершин
    vert_string = ""
    for i in range(vert_count):
        vert_string += str(i)
    #генерация линий
    for i in itertools.combinations(vert_string,2):
        if randrange(0,2):
            linkcost = randrange(1,10)
            if linkcost > 5:
                sm = 20
            else:
                sm = -20
            canv.create_line(vert_array[int(i[0])].x,vert_array[int(i[0])].y,vert_array[int(i[1])].x,vert_array[int(i[1])].y,width=2,tag="lines")
            canv.create_text((((vert_array[int(i[0])].x+vert_array[int(i[1])].x)/2+5)),((vert_array[int(i[0])].y+vert_array[int(i[1])].y)/2 + sm),text=str(linkcost),fill="green",font="Arial 14",tag="labels")
            #создание объекта связки с началом, концом и стоимостью
            link = Link(vert_array[int(i[0])],vert_array[int(i[1])],linkcost)
            link_array.append(link)

    #отрисовка вершин поверх линий
    for item in vert_array:
        #удалить метки со стоимостью перехода
        canv.delete("label"+str(item.number))
        #обнуление стоимости всех вершин
        item.cost = 9999
        item.hold = 0
        canv.create_oval(item.x-15, item.y-15, item.x+15, item.y+15, fill="white", outline="black", width = 2, tag="vert"+str(item.number))
        canv.create_text(item.x, item.y, text = str(item.number + 1), tag = "labels", font = "Arial 14")

    btn2["state"] = DISABLED
    lbl["text"] = "Выберите стартовую точку"

#функция установления начальной точки
def click(e):
    global start_vertex
    #проверка, не установлена ли вершина до клика
    status = 0
    for item in vert_array:
        if item.cost == 0:
            status = 1

    #если вершина не была установлена ранее, перекрасить овал в зелёный цвет
    if status == 0:
        for item in vert_array:
            if item.x >= e.x - 15 and item.x <= e.x + 15 and item.y >= e.y - 15 and item.y <= e.y + 15:
                item.cost = 0
                #перекрасить вершину в зелёный
                canv.itemconfig("vert"+str(item.number),fill="green")
                #добавить текст со стоимостью перехода в вершину
                canv.create_text(item.x - 15, item.y - 20, text = "0", tag = "labels", font = "Arial 14", fill = "red")
                lbl["text"] = ""
                btn2["state"] = ACTIVE
                break

#функция нахождения всех соседей вершины (на входе вершины, на выходе массив вершин, с которыми она соседствует и длиной до них
def getNeighbors(vertex):
    neighbors = []
    for link in link_array:
        #если номер вершины совпадает с номером вершины начала связи, то записать вершину конца в массив соседей
        if vertex.number == link.begin.number:
            neighbors.append([link.end,link.length])
        elif vertex.number == link.end.number:
            neighbors.append([link.begin,link.length])
    return neighbors

#функция проверки, все ли точки заблокированы (1 - не все заблокированы, 0 - заблокированы все)
def checkHold():
    status = 0
    for item in vert_array:
        status += item.hold

    if status != len(vert_array):
        return 1
    else:
        return 0

#запуск алгоритма Дейкстры
def play():
    #найти стартовую вершину
    for item in vert_array:
        if item.cost == 0:
            start_vertex = item
            break

    #попытки. Если количество попыток превыщает количество вершин, то выход из алгоритма
    attempts = 0
    #начинаем обход по вершинам, пока они все не будут заблокированы
    while checkHold():
        attempts += 1

        #if attempts > len(vert_array) + 1:
        if attempts > 50:
            lbl["text"] = "Готово"
            print(attempts)
            break

        min_length = 9999
        #найти следующую вершину из соседей
        for neighbors in getNeighbors(start_vertex):
            if neighbors[1] < min_length and neighbors[0].hold == 0:
                next_vertex = neighbors[0]
                min_length = neighbors[1]

        #если происходит постоянное зацикливание - то выходить
        if next_vertex.number == start_vertex.number:
            break

        #проход по соседям и пересчёт стоимости перехода в них
        for neighbors in getNeighbors(start_vertex):
            if neighbors[0].hold == 0:
                if start_vertex.cost + neighbors[1] < neighbors[0].cost:
                    neighbors[0].cost = start_vertex.cost + neighbors[1]
                    #удалить старую метку
                    canv.delete("label"+str(neighbors[0].number))
                    #добавить текст со стоимостью перехода в вершину
                    canv.create_text(neighbors[0].x - 15, neighbors[0].y - 20, text = str(neighbors[0].cost)+"_"+str(attempts), tag = "label"+str(neighbors[0].number), font = "Arial 14", fill = "red")

        start_vertex.hold = 1
        canv.itemconfig("vert"+str(next_vertex.number),fill="yellow")
        start_vertex = next_vertex


#создание окна для размещения вершин графа 
root = Tk() 
root.geometry("600x600+300+0")
root.title("Dijkstra algorithm")
  
#холст для вершин графа
canv = Canvas(root, width = 600,height = 500, bg = "white")
canv.pack()

#Добавление надписи
lbl = Label(root)
lbl["font"] = "Arial 14"
lbl["text"] = ""
lbl.pack() 

#Добавление кнопки для отрисовки линий между вершинами
btn1 = Button(root)
btn1["width"] = 200
btn1["command"] = reset 
btn1["text"] = "Шаг1. Сгенерировать поле"
btn1.pack() 

#Добавление кнопки для запуска алгоритма Дейкстры
btn2 = Button(root)
btn2["width"] = 200
btn2["state"] = DISABLED
btn2["command"] = play
btn2["text"] = "Запустить алгоритм"
btn2.pack()

#добавить слушателя на клик мыши 
root.bind("<Button-1>", click)

#инициализация меню для главного окна
m = Menu(root)
#указать главному окну, как называется меню
root.config(menu = m)

#создание элемента меню главного меню
fm = Menu(m)
#добавить на главное меню раскрывающееся меню
m.add_cascade(label="Визуализатор",menu = fm)
#добавить элементы в раскрывающееся меню fm
fm.add_command(label="Настройка", command = settings)

hm = Menu(m)
m.add_cascade(label="Справка",menu = hm)
hm.add_command(label="О программе",command = about)

root.mainloop()
