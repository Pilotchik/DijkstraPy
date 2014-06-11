__author__ = 'Александр'

class Vertex():
    cost = 9999
    hold = 0

    def __init__(self,cost):
        self.cost = cost

class Link():
    begin = 0
    end = 0
    length = 0

    def __init__(self,begin,end,length):
        self.begin = begin
        self.end = end
        self.length = length