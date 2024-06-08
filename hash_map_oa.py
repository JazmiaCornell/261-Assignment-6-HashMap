# Name: Jazmia Cornell
# OSU Email: cornellj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06
# Due Date: 06/06/2024
# Description: The following functions are designed to implement a HashMap utilizing open addressing
#                for collision resolution

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        # calculates load factor
        load_factor = self._size / self._capacity
        # if >= .5, resizes table
        if load_factor >= 0.5:
            self.resize_table(self._capacity * 2)
        # creates entry for hash map
        temp = HashEntry(key, value)
        # calculates initial index
        index = (self._hash_function(key) % self._capacity)
        i = 0

        while True:
            quad_prob = (index + (i ** 2)) % self._capacity
            hash_entry = self._buckets.get_at_index(quad_prob)
            # if position is empty or is a tombstone (placeholder), sets entry at calc index, increases size
            if hash_entry is None or hash_entry.is_tombstone:
                self._buckets.set_at_index(quad_prob, temp)
                self._size += 1
                return
            # if key already exists, replaces old value with new
            elif hash_entry.key == key:
                hash_entry.value = value
                return
            # if not empty or key not found, go to next position
            i += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        # checks if new capacity is < elements in map
        if new_capacity < self._size:
            return

        load_factor = self._size / new_capacity

        # if new_capacity is < size, finds next prime if not and doubles if nec.
        while load_factor >= 0.5:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            load_factor = self._size / new_capacity
            if load_factor >= 0.5:
                new_capacity = 2 * new_capacity
            else:
                break
        # ensures new_capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # creates new map
        temp = DynamicArray()
        # initializes new map
        for i in range(new_capacity):
            temp.append(None)

        # moves old values to new map
        for i in range(self._capacity):
            # iterates through old array
            bucket = self._buckets.get_at_index(i)
            # if bucket found, calculates new index (to move value to new array)
            if bucket and not bucket.is_tombstone:
                index = self._hash_function(bucket.key) % new_capacity
                j = 0
                while True:
                    quad_prob = (index + (j ** 2)) % new_capacity
                    hash_entry = temp.get_at_index(quad_prob)
                    # if position is empty or is a tombstone (placeholder), sets entry at calc index, increases size
                    if hash_entry is None or hash_entry.is_tombstone:
                        temp.set_at_index(quad_prob, bucket)
                        break
                    j += 1

        # sets buckets to new map and capacity to new_capacity
        self._capacity = new_capacity
        self._buckets = temp


    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """

        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        # calculates initial index
        index = self._hash_function(key) % self._capacity
        i = 0

        while True:
            # quadratic probing
            quad_prob = (index + (i ** 2)) % self._capacity
            hash_entry = self._buckets.get_at_index(quad_prob)
            # if position is empty or has a placeholder, return None
            if hash_entry is None or hash_entry.is_tombstone:
                return None
            # elif key is found return value
            elif hash_entry.key == key:
                return hash_entry.value
            # if not found, go to next position
            i += 1

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """

        if self.get(key) is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        # calculates initial index
        index = self._hash_function(key) % self._capacity
        i = 0

        while True:
            # quadratic probing
            quad_prob = (index + (i ** 2)) % self._capacity
            hash_entry = self._buckets.get_at_index(quad_prob)
            # if position is empty returns None
            if hash_entry is None:
                return None
            # elif key is found set tombstone to true, decrease size
            elif hash_entry.key == key and not hash_entry.is_tombstone:
                hash_entry.is_tombstone = True
                self._size -= 1
            # if not found, go to next position
            i += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        # creates dynamic array
        pairs = DynamicArray()

        # iterates through capacity size
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            # if bucket has value
            if bucket:
                # creates tuple of key/value pair and adds to pair array
                if not bucket.is_tombstone:
                    pair_tuple = (bucket.key, bucket.value)
                    pairs.append(pair_tuple)
                else:
                    i += 1

        return pairs

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        # create a new array (empty buckets)
        temp = DynamicArray()

        # appends None to each bucket
        for i in range(self._capacity):
            temp.append(None)

        # set size = 0, and buckets to temp
        self._buckets = temp
        self._size = 0

    def __iter__(self):
        """
        Creates iterator for loop
        """
        # initializes index at 0
        self._index = 0

        return self

    def __next__(self):
        """
        Obtains next value and advance iterator
        """
        # goes through array, returning buckets that have key/value pairs
        while self._index < self._capacity:
            temp = self._buckets.get_at_index(self._index)
            self._index += 1
            if temp and not temp.is_tombstone:
                return temp

        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(111)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(162, hash_function_2)
    keys = [i for i in range(0, 75, 1)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(111)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
