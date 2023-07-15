lista = ['jf', 'ariel', 'gallo']

class Character:
    def __init__(self, name):
        self.name = name
        self.inic = None

    def get_name(self):
        return self.name

    def set_inic(self, value):
        self.inic = value

    def get_inic(self):
        return self.inic

characters = []

for name in lista:
    name = Character(name)
    characters.append(name)

for item in characters:
    print(type(item))
    print(item.get_name())