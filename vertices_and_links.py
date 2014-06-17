__author__ = 'Александр Кудрявцев'

#класс для вершин графа
class Vertex():

    #стоимость
    cost = 9999
    #статус блокировки
    hold = 0
    #координаты центра на холсте
    x = 0
    y = 0
    #порядковый номер
    number = 0

    def __init__(self,cost = 9999, x = 0, y = 0, number = 0):
        self.cost = cost
        self.x = x
        self.y = y
        self.number = number

#класс для свойств и методов связей
class Link():
    begin = 0
    end = 0
    length = 0

    def __init__(self,begin,end,length):
        self.begin = begin
        self.end = end
        self.length = length
