"""
Input Register
Входные регистры ModbusTCP
OnlyRead
"""



class InputRegister:
    _instance = None #Экземпляр класса
    lInputRegisters = dict()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls,*args,**kwargs)
        return cls._instance


    def addToRegister(self, Register, Value, Info):
        self.lInputRegisters[Register] = [Value, Info]