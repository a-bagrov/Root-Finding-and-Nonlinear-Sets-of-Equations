class BinarySearch:

    @staticmethod
    def binary_search(sorted_tuple_list, value, start_index=0, length=None):
        lo = start_index
        if length is None:
            hi = len(sorted_tuple_list) - 1
        else:
            hi = start_index + length - 1

        while lo <= hi:
            i = lo + ((hi - lo) >> 1)
            c = sorted_tuple_list[i][0]
            if c == value:
                return i

            if c < value:
                lo = i + 1
            else:
                hi = i - 1

        return ~lo
