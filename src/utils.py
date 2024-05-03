import numpy as np

from src.debug_utils import print_high


class Utils:
    @staticmethod
    def permute(lst):
        # return [lst]

        # If lst is empty then there are no permutations
        if len(lst) == 0:
            return []

        # If there is only one element in lst then, only
        # one permutation is possible
        if len(lst) == 1:
            return [lst]

        # Find the permutations for lst if there are
        # more than 1 characters

        l = [] # empty list that will store current permutation

        # Iterate the input(lst) and calculate the permutation
        for i in range(len(lst)):
           m = lst[i]

           # Extract lst[i] or m from the list.  remLst is
           # remaining list
           remLst = lst[:i] + lst[i+1:]

           # Generating all permutations where m is first
           # element
           for p in Utils.permute(remLst):
               l.append([m] + p)

        return l

    @staticmethod
    def addValues(initEl):
        import numpy as np

        sortedEl = Utils.sort_lambda(initEl, lambda a, b: b - a)
        permuted_sorted = np.concatenate((
            Utils.permute([sortedEl[0], sortedEl[1], sortedEl[2]]),
            Utils.permute([-sortedEl[0], sortedEl[1], sortedEl[2]]),
            Utils.permute([sortedEl[0], -sortedEl[1], sortedEl[2]]),
            Utils.permute([sortedEl[0], sortedEl[1], -sortedEl[2]]),
            Utils.permute([-sortedEl[0], -sortedEl[1], sortedEl[2]]),
            Utils.permute([-sortedEl[0], sortedEl[1], -sortedEl[2]]),
            Utils.permute([sortedEl[0], -sortedEl[1], -sortedEl[2]]),
            Utils.permute([-sortedEl[0], -sortedEl[1], -sortedEl[2]])))
        unique_permuted_sorted = Utils.unique_no_sort(permuted_sorted)

        return unique_permuted_sorted

    @staticmethod
    def hasSimilar (invariants, buffer, item):
        print_high("!!!!!!!!!!!!!!!!!!!!!!!!!_____hasSimilar______!!!!!!!!!!!!------")
        print_high(invariants)
        print_high(buffer)
        print_high(item)
        for i in range(len(invariants)):
            invariants_i = np.array(invariants[i])
            _sum = np.array(item) + invariants_i
            _diff = invariants_i - np.array(item)
            buffer_arr = np.array(buffer)
            if Utils.check_2d_array_contains_1d_array(buffer_arr, _sum) or Utils.check_2d_array_contains_1d_array(buffer_arr, _diff):
                print_high(",,,,,,,,,,,,,,,,,,,,,,,,,,,_____TRUE______!!!!!!!!!!!!------")
                return True

        print_high(",,,,,,,,,,,,,,,,,,,,,,,,,,,_____FALSE______!!!!!!!!!!!!------")
        return False

    @staticmethod
    def check_2d_array_contains_1d_array(array_2d, array_1d):
        is_contains = any(np.array_equal(x, array_1d) for x in array_2d)

        return is_contains

    @staticmethod
    def checkInQueue (invariants, queue, item, allowInvariants):
        _invariants = Utils.addValues(item)
        print_high(invariants)
        print_high(queue)
        print_high(item)
        for i in range(len(_invariants)):
            if not allowInvariants and Utils.hasSimilar(invariants, queue, _invariants[i]):
                print_high("TRUE")
                return True
        print_high("FALSE")
        return False

    @staticmethod
    def sortingGroups(group1, group2):
        n1 = Utils.findN2(group1)
        n2 = Utils.findN2(group2)
        if n1 == n2:
            if Utils.inLimit(group1, group2):
                return -1
            elif Utils.inLimit(group2, group1):
                return 1
            else:
                return 0
        else:
            result = n1 - n2

        return result

    @staticmethod
    def sort_lambda(array, _lambda):
        from functools import cmp_to_key
        result = sorted(array, key=cmp_to_key(_lambda))

        return result

    @staticmethod
    def inLimit(value, maxLimit):
        curValue = Utils.sort_lambda([abs(value[0]), abs(value[1]), abs(value[2])], lambda a, b: b - a)
        curLimit = Utils.sort_lambda([abs(maxLimit[0]), abs(maxLimit[1]), abs(maxLimit[2])], lambda a, b: b - a)
        expression = f'"{curValue[0]}{curValue[1]}{curValue[2]}"<"{curLimit[0]}{curLimit[1]}{curLimit[2]}"'
        result = eval(expression)

        return result

    @staticmethod
    def extractInvariants (invariants, maxValue, l, allowInvariants):
        print_high(invariants)
        print_high(maxValue)  #!!!!!!!Useless!!!!!!!
        print_high(l)
        print_high(allowInvariants)

        results = []
        for i in range(len(l)):
            if allowInvariants or not Utils.hasSimilar(invariants, results, l[i]):
                results.append(list(l[i]))

        return results

    @staticmethod
    def findN2(pos):
        return pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2

    @staticmethod
    def flatten(buffer, multiplier):
        flattened = [item for sublist in buffer for item in sublist]
        flattened_multiplied = flattened * multiplier

        return flattened_multiplied

    @staticmethod
    def print_list_of_vectors_in_row(array):
        buffer = ""
        for i in range(len(array)):
            buffer = f'{buffer}{i+1} {array[i]} \n'

        print(buffer)

    @staticmethod
    def print_list_of_vectors_in_line(array):
        buffer = Utils.build_string_list_of_vectors_in_line(array)

        print(buffer)

    @staticmethod
    def build_string_list_of_vectors_in_line(array):
        string = "".join(["[", ', '.join(str(f'[{", ".join(str(x) for x in y)}]') for y in array), "]"])

        return string

    @staticmethod
    def unique_no_sort(array):
        indexes = np.unique(array, return_index=True, axis=0)[1]
        result = [array[index] for index in sorted(indexes)]

        return result
