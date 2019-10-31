import numpy as np


class OLA_CAL_READER:
    def __init__(self, fname):
        self.fname = fname
        self.read_lines()
        self.get_indices()
        self.parse_range_coeffs()
        self.parse_az_el_coeffs()
        self.parse_rest()

    def read_lines(self):
        data = []
        with open(self.fname) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue
                data.append(line)
        self.data = data

    def get_indices(self):
        indices = []
        for i, line in enumerate(self.data):
            if line.split()[0].isupper():
                indices.append(i)
        self.indices = indices

    def parse_group_to_array(self, index):
        group = self.data[self.indices[index] + 1:self.indices[index + 1]]
        bucket = []
        for line in group:
            bucket.extend(np.array(line.strip('\\').split(), dtype='float'))
        return np.array(bucket)

    def parse_range_coeffs(self):
        self.RANGE_HELT_FIXED = float(self.data[0].split()[1])
        self.RANGE_HELT_LUT = self.parse_group_to_array(0)
        self.RANGE_LELT_FIXED = float(self.data[self.indices[1]].split()[1])
        self.RANGE_LELT_LUT = self.parse_group_to_array(1)

    def parse_az_el_coeffs(self):
        self.AZIMUTH_HELT = self.parse_group_to_array(2)
        self.AZIMUTH_LELT = self.parse_group_to_array(3)
        self.ELEVATION_HELT = self.parse_group_to_array(4)
        self.ELEVATION_LELT = self.parse_group_to_array(5)

    def parse_rest(self):
        for index in self.indices[6:]:
            tokens = self.data[index].split()
            setattr(self, tokens[0], np.array(tokens[1:], dtype='float'))
