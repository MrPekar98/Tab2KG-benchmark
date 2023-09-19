class Stats:
    def __init__(self):
        self.__rows = 0
        self.__columns = 0
        self.__entities = 0
        self.__entities_in_kg = 0

    def rows(self):
        return self.__rows

    def columns(self):
        return self.__columns

    def entities(self):
        return self.__entities

    def entity_coverage(self):
        return self.__entities_in_kg

    def set_rows(self, rows):
        self.__rows = rows

    def set_columns(self, columns):
        self.__columns = columns

    def set_num_entities(self, num):
        self.__entities = num

    def set_num_covered_entities(self, num):
        self.__entities_in_kg = num

    def print(self):
        print('Avg #rows: ' + str(self.__rows))
        print('Avg #columns: ' + str(self.__columns))
        print('Avg #entities: ' + str(self.__entities))

        if self.__entities > 0:
            print('Avg ground truth entity coverage: ' + str((self.__entities_in_kg / self.__entities) * 100))

        else:
            print('Avg ground truth entity coverage: 0.0%')
