class Stats:
    def __init__(self):
        self.__rows = 0
        self.__columns = 0
        self.__entities = 0
        self.__entities_in_kg = 0
        self.__tables = 0
        self.__entity_density = 0

    def tables(self):
        return self.__tables

    def rows(self):
        return self.__rows

    def columns(self):
        return self.__columns

    def entities(self):
        return self.__entities

    def entity_density(self):
        return self.__entity_density

    def set_tables(self, num):
        self.__tables = num

    def set_rows(self, rows):
        self.__rows = rows

    def set_columns(self, columns):
        self.__columns = columns

    def set_num_entities(self, num):
        self.__entities = num

    def set_entity_density(self, density):
        self.__entity_density = density

    def print(self):
        print('#tables: ' + str(self.__tables))
        print('Avg #rows: ' + str(self.__rows))
        print('Avg #columns: ' + str(self.__columns))
        print('Avg #entities: ' + str(self.__entities))
        print('Avg entity density: ' + str(self.__entity_density))
