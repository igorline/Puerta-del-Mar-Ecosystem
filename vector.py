import operator as op
import math

class Vector:
    # TODO: Finish the Vector class.
    def __init__(self, array=[]):
        self.__data = array
  
    def __len__(self):
        return len(self.__data)
    
    def __iter__(self):
        return iter(self.__data)
    
    def __getitem__(self, i):
        return self.__data[i]
    
    def __asign__(self, value):
        self.__data = value.__data
    
    def check_length(f):
        def wrapper(self, other):
            if len(self) != len(other):
                raise ValueError()
            return f(self, other)
        return wrapper
    
    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        try:
            return self[2]
        except IndexError:
            return None
    
    @check_length
    def add(self, other):
        # self.__data = Vector(map(op.add, self, other)).__data
        res = Vector(map(op.add, self, other))
        return res

  
    @check_length
    def subtract(self, other):
        res = Vector(map(op.sub, self, other))
        return res

    def sub(self, other):
        return self.subtract(other)
    
    @check_length  
    def dot(self, other):
        res = reduce(op.add, imap(op.mul, self, other))
        return res

    def div(self, n):
        return Vector([x / n for x in self.__data])

    def mult(self, n):
        return Vector([x * n for x in self.__data])

    def dist(self, v):
        dx = self.x - v.x
        dy = self.y - v.y
        if (self.z):
            dz = self.z - v.z
            return sqrt(dx * dx + dy * dy + dz * dz)

        return sqrt(dx * dx + dy * dy)


    def setMag(self, len):
        return self.normalize().mult(len)

            

        
    
    def norm(self):
        return sqrt(self.dot(self))
    
    def equals(self, other):
        if len(self) != len(other):
            return False
        return all(map(op.eq, self, other))

    def limit(self, max):
        if (self.magSq() > max*max):
            return self.normalize().mult(max)
        print self
        return self

    def normalize(self):
        m = self.mag()
        if (m != 0.0 and m != 1):
            return self.div(m)
        else:
            return self

    
    def __str__(self):
        return '(%s)' % ','.join(str(x) for x in self.__data)

    def mag(self):
        if not self.z:
            return math.sqrt(self.x*self.x + self.y*self.y);
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z);

    def magSq(self):
        if not self.z:
            return self.x*self.x + self.y*self.y
        return self.x*self.x + self.y*self.y + self.z*self.z

    @property
    def heading(self):
        angle = math.atan2(-self.y, self.x);
        return -1*angle

