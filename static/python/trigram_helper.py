from enum import Enum


class TrigramOutput(Enum):
    ASCII = "ASCII",
    BASE64 = "BASE64"


class TrigramReadMode(Enum):
    ACB = 'acb'
    ABC = 'abc'
    BAC = 'bac'
    BCA = 'bca'
    CAB = 'cab'
    CBA = 'cba'

    def print_data(self, a, b, c):
        return self.value.replace('a', a).replace('b', b).replace('c', c)

    def calculate_value(self, a, b, c):
        data = self.print_data(a, b, c)
        return str(int(data, 5))

    def convert_to_raw(self, a1, a2, a3):
        chars = [None, None, None]
        chars[self.value.index('a')] = a1  # 2 // index 1
        chars[self.value.index('b')] = a2  # 3 // index 3
        chars[self.value.index('c')] = a3  # 1 // index 2
        return ''.join(chars)


class Trigram:
    def __init__(self, trigram):
        self.a, self.b, self.c = trigram

    def get_trigram_value(self, mode):
        return mode.calculate_value(self.a, self.b, self.c)

    def get_trigram_string(self, mode):
        return mode.print_data(self.a, self.b, self.c)


class EyeData:
    def __init__(self, name, eye_data, selected_mode=TrigramReadMode.ACB):
        self.message = name
        self.eye_line_data = [list(line) for line in eye_data.split('5')]
        self.trigram_line_data = []
        self.selected_mode = TrigramReadMode(selected_mode)
        self.calculate_trigrams_from_raw()

    def calculate_trigrams_from_raw(self):
        raw_trigram_data = []
        for i in range(0, len(self.eye_line_data) - 1, 2):
            line_a = self.eye_line_data[i]
            line_b = self.eye_line_data[i + 1]
            line_a_index, line_b_index = 0, 0
            new_data = ''
            while line_a_index < len(line_a) or line_b_index < len(line_b):
                if line_a_index < len(line_a):
                    new_data += line_a[line_a_index]
                    line_a_index += 1

                if line_b_index < len(line_b):
                    new_data += line_b[line_b_index]
                    line_b_index += 1
            raw_trigram_line_data = '\n'.join([new_data[i:i + 3] for i in range(0, len(new_data), 3)])
            raw_trigram_data.append(raw_trigram_line_data)

        for trigram_line in raw_trigram_data:
            trigrams = trigram_line.split('\n')
            raw_line_data = [Trigram(trigram) if i % 2 == 0 else Trigram(trigram[::-1]) for i, trigram in
                             enumerate(trigrams)]
            self.trigram_line_data.append(raw_line_data)

    def get_raw_eye_data(self):
        return self.convert_to_string(self.eye_line_data)

    def get_raw_trigram_data(self):
        return '\n'.join([','.join([trigram.get_trigram_string(self.selected_mode) for trigram in line]) for line in
                          self.trigram_line_data])

    def get_trigram_values(self):
        return '\n'.join([','.join([trigram.get_trigram_value(self.selected_mode) for trigram in line]) for line in
                          self.trigram_line_data])

    @staticmethod
    def convert_to_string(lst):
        return '\n'.join([''.join(inner_list) for inner_list in lst])
