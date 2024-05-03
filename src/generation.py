import math
import numpy as np

from src.debug_utils import print_high
from src.utils import Utils


class Generation:
    def __init__(self, N, startFrom, endTo, allowInvariants=False, multiplier=1):
        self.N = N
        self.startFrom = startFrom
        self.endTo = endTo
        self.buffer = [[[0, 0, 0]]]
        self.count = 0
        self.multiplier = multiplier
        self.detectType()
        variantQueue = [self.modifier]
        currentIndex = 0
        checked = variantQueue[currentIndex]
        mutators = Utils.addValues(self.modifier)
        currentBarrier = Utils.findN2(checked)
        cache = []

        print_high(self.modifier)
        print_high(self.maxValue)
        print_high(f'self.maxValue={self.maxValue}')
        print_high(self.maxBarrier)
        print_high(f'self.invariants={Utils.build_string_list_of_vectors_in_line(self.invariants)}')
        print_high(len(self.invariants));
        print_high(np.sum(self.invariants, axis=0))
        print_high(self.modifier)
        print_high(variantQueue)
        print_high(checked)
        print_high(f'mutators={Utils.build_string_list_of_vectors_in_line(mutators)}')
        print_high(len(mutators))
        print_high(currentBarrier)

        while currentBarrier < self.maxBarrier and self.inLimit(checked):
            print_high(f"=========={currentIndex+1}=========")
            checked_add_vals = Utils.addValues(checked)
            curValues = Utils.extractInvariants(self.invariants, self.maxValue, checked_add_vals, allowInvariants)

            print_high(f'checked={checked}')
            print_high(f'checked_add_vals={Utils.build_string_list_of_vectors_in_line(checked_add_vals)}')
            print_high(f'curValues={curValues}')

            self.buffer.append(curValues)
            self.count = self.count + len(curValues)
            for i in range(len(mutators)):
                print_high(f"----------{currentIndex+1}/{i+1}---------")

                print_high(f'checked={checked}')
                print_high(f'mutators[i]={mutators[i]}')

                possibleStep = list(checked + mutators[i])

                print_high(f'possibleStep={possibleStep}')

                n2 = Utils.findN2(possibleStep)

                print_high(f'n2={n2}')
                print_high(f'currentBarrier={currentBarrier}')

                if n2 > currentBarrier:
                    general = Utils.sort_lambda([abs(possibleStep[0]), abs(possibleStep[1]), abs(possibleStep[2])], lambda a, b: b - a)

                    print_high(f'general={general}')
                    print_high(f'cache={cache}')

                    if not Utils.check_2d_array_contains_1d_array(cache, general):
                        print_high("not Utils.check_2d_array_contains_1d_array(cache, general)")
                        cache.append(general)
                        stepBarrier = Utils.findN2(possibleStep)

                        print_high(f'stepBarrier={stepBarrier}')
                        print_high(f'variantQueue={variantQueue}')

                        in_queue = self.checkInQueue(variantQueue, possibleStep, allowInvariants)
                        in_barrier = stepBarrier < self.maxBarrier
                        in_limit = self.inLimit(possibleStep)

                        print_high(f'in_queue={in_queue}')
                        print_high(f'in_barrier={in_barrier}')
                        print_high(f'in_limit={in_limit}')

                        if not in_queue and in_barrier and in_limit:
                            variantQueue.append(possibleStep)
                            print_high(f'!!!!!!!!!!!variantQueue!!!!!!!!!!!={Utils.build_string_list_of_vectors_in_line(variantQueue)}')
                    else:
                        print_high("HAS")

            print_high(f'variantQueue_1={Utils.build_string_list_of_vectors_in_line(variantQueue)}')

            variantQueue = Utils.sort_lambda(variantQueue, Utils.sortingGroups)

            print_high(f'variantQueue_2={Utils.build_string_list_of_vectors_in_line(variantQueue)}')

            currentIndex = currentIndex + 1
            if len(variantQueue) <= currentIndex:
                print_high("len(variantQueue) <= currentIndex")
                currentBarrier = math.inf
            else:
                print_high("len(variantQueue) > currentIndex")
                checked = variantQueue[currentIndex]
                currentBarrier = Utils.findN2(checked)

            print_high(f"====================")

    def detectType(self):
        tModifiers = {
            "PKR": [1, 0, 0],
            "GCK": [1, 1, 0],
            "OCK": [1, 1, 1],
        }
        tBarriers = {
            "PKR": np.asarray([self.N, 0, 0], dtype = 'int'),
            "GCK": np.asarray([self.N / 2, self.N / 2, 0], dtype = 'int'),
            "OCK": np.asarray([self.N / 2, self.N / 2, self.N / 2], dtype = 'int'),
        }
        tInvariants = {
            "PKR": np.asarray(np.concatenate((
                Utils.addValues([self.N, 0, 0]),
                Utils.addValues([self.N, self.N, 0]),
                Utils.addValues([self.N, self.N, self.N]),
                Utils.addValues([2 * self.N, self.N, self.N]),
                Utils.addValues([2 * self.N, 2 * self.N, self.N]),
                Utils.addValues([2 * self.N, 2 * self.N, 2 * self.N]),
                Utils.addValues([2 * self.N, 0, 0]),
                Utils.addValues([2 * self.N, self.N, 0]),
            ), axis=0), dtype = 'int'),
            "GCK": np.asarray(np.concatenate((
                Utils.addValues([self.N / 2, self.N / 2, 0]),
                Utils.addValues([self.N, self.N, 0]),
                Utils.addValues([self.N, self.N / 2, self.N / 2]),
                Utils.addValues([self.N, 0, 0]),
                Utils.addValues([self.N, self.N, self.N]),
            ), axis=0), dtype = 'int'),
            "OCK": np.asarray(np.concatenate((
                Utils.addValues([self.N / 2, self.N / 2, self.N / 2]),
                Utils.addValues([self.N, self.N, self.N]),
                Utils.addValues([self.N, self.N, 0]),
                Utils.addValues([self.N, 0, 0]),
            ), axis=0), dtype = 'int'),
        }
        self.modifier = tModifiers[self.startFrom]
        self.maxValue = tBarriers[self.endTo]
        self.maxBarrier = Utils.findN2(self.maxValue)
        self.invariants = tInvariants[self.endTo]

    @staticmethod
    def sort_lambda(array, _lambda):
        from functools import cmp_to_key
        result = sorted(array, key=cmp_to_key(_lambda))

        return result

    def inLimit (self, checked):
        res = Utils.inLimit(checked, self.maxValue)

        return res

    def checkInQueue (self, queue, item, allowInvariants):
        res = Utils.checkInQueue(self.invariants, queue, item, allowInvariants)

        return res

    def flatten(self):
        res = Utils.flatten(self.buffer, self.multiplier)

        return res