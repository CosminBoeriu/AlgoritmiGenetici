import math

class Chromosome:
    interval = (-10, 10)
    precision = 6
    number_of_bits = math.ceil(math.log2((interval[1] - interval[0]) * (10 ** precision)))
    bucket = (interval[1] - interval[0]) / (2 ** number_of_bits)

    def __init__(self, value):
        self._value = value
        self._encoded_value = Chromosome.encode_float_to_bit_representation(self._value)

    def __str__(self):
        return self._value

    @staticmethod
    def encode_float_to_bit_representation(value):
        value = math.floor((value - Chromosome.interval[0]) / Chromosome.bucket)
        return value

    @staticmethod
    def decode_bit_representation_to_float(value):
        return Chromosome.interval[0] + value * Chromosome.bucket

    def get_value(self):
        return self._value

    def get_segment_of_bits(self, start, num_of_bits):
        return self._encoded_value & (((1 << num_of_bits) - 1) << start)

    def flip_bit(self, position):
        bit_pos = 1 << position
        if self._encoded_value & bit_pos == 0:
            return Chromosome(self.decode_bit_representation_to_float(self._encoded_value + bit_pos))
        else:
            return Chromosome(self.decode_bit_representation_to_float(self._encoded_value ^ bit_pos))
