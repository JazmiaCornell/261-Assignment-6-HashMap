# Name: Jazmia Cornell
# OSU Email: cornellj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06
# Due Date: 06/06/2024
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Returns a hash map with the passed key/value pair. If a value exists at the calculated index
        (from hash function), override the value with the passed value. Else, create a new key/value pair
        at calculated index.

        :param key: a string that is passed and is used to calculate the index
        :param value: an object that is passed and is set as a key/value pair to the key

        :return: an updated hash map with the passed key/value pair added at the calculated index
        """

        # calculate load factor
        load_factor = (self._size / self._capacity)

        # if load factor is >= 1, double capacity of hash map
        if load_factor >= 1:
            new_capacity = 2 * self._capacity
            self.resize_table(new_capacity)

        # calculate the index that the value needs to be inserted into map
        hash_calc = self._hash_function(key)
        index = hash_calc % self._capacity

        # find bucket
        bucket = self._buckets.get_at_index(index)

        # if the bucket exists at desired index continue to node
        if bucket:
            node = bucket.contains(key)
            # if node exists with same key, override with new value
            if node:
                node.value = value
            # else create a new node in SLL
            else:
                bucket.insert(key, value)
                self._size += 1
        # else create new bucket with key/value pair set at index
        else:
            new_bucket = LinkedList()
            new_bucket.insert(key, value)
            self._buckets.set_at_index(index, new_bucket)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Doubles the capacity of hash map and moves existing key/value pairs to new map (rehash).

        :param new_capacity: an integer that is the new_capacity (2 * self._capacity)

        :return: a new hash map with double the capacity size but same key/value pairs as the old map
        """
        # if new_capacity is negative, return
        if new_capacity < 1:
            return

        # while new_capacity < self._size:
        #     new_capacity = 2 * new_capacity
        #
        # load_factor = self._size / new_capacity
        #
        # while load_factor >= 1:
        #     new_capacity = new_capacity * 2

        # if new_capacity is not prime, calculates next prime number and sets to new_capacity
        while not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # creates a new hash map (buckets) and append linked list for each index (to capacity)
        new_hash = DynamicArray()
        for i in range(new_capacity):
            new_hash.append(LinkedList())

        # move key/value pairs from old array to new array
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            # if node in linked list at index, move node to new linked list
            for node in bucket:
                new_index = self._hash_function(node.key) % new_capacity
                new_bucket = new_hash.get_at_index(new_index)
                new_bucket.insert(node.key, node.value)

        # set new map and capacity to self
        self._buckets = new_hash
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Returns the current load factor for the hash map

        :return: a float value that is the current load factor
        """
        # calculates the load factor, number of elements / capacity
        load_factor = self._size / self._capacity

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash map.

        :return: an integer that is the number of empty buckets
        """
        # set empty_buckets to 0
        empty_buckets = 0

        # in range of array size, if bucket length == 0 (is empty) at i, +1 to empty_bucket total
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            if bucket.length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str):
        """
        Returns the value associated with a given key, else returns None.

        :param key: a string that is passed and used to calculate the bucket(index) to search for
        a key/value pair.

        :return: a value that is associated with the passed key.
        """
        # calculate the index that the value needs to be inserted into map
        hash_calc = self._hash_function(key)
        index = hash_calc % self._capacity

        # find bucket
        bucket = self._buckets.get_at_index(index)

        # if the bucket exists at desired index continue to node
        if bucket:
            node = bucket.contains(key)
            # if key at given node == passed key return the value, else return None
            if node:
                if node.key == key:
                    return node.value
                else:
                    return None
            else:
                return None
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is within the hash map, else returns False.

        :param key: a passed string that is given to find within the map and calculate the index

        :return: a Boolean object depending on if the given key is found or not
        """
        # calculate the index that the value needs to be inserted into map
        hash_calc = self._hash_function(key)
        index = hash_calc % self._capacity

        # find bucket
        bucket = self._buckets.get_at_index(index)

        # if the bucket exists at desired index continue to node
        if bucket.contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Returns an updated hash map with removed key (passed).

        :param key: a passed string that is looked for in the hash, if found removed.

        :return: an updated hash with the passed key removed
        """
        # calculate the index that the value needs to be inserted into map
        hash_calc = self._hash_function(key)
        index = hash_calc % self._capacity

        # find bucket
        bucket = self._buckets.get_at_index(index)

        # if the bucket exists at desired index continue to node
        if bucket:
            node = bucket.contains(key)
            # if key at given node == passed key remove key/value pair, else return
            if node and node.key == key:
                bucket.remove(key)
                self._size -= 1
            else:
                return
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray of key/value pairs within a hash.

        :return: a dynamic array that contains tuples of key/value pairs from a hash map
        """
        # initializes array
        pairs = DynamicArray()

        # iterates through buckets
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            # if linked_list exists at bucket
            if bucket:
                for node in bucket:
                    # if node in linked_list, add the key/value to tuple and append to pairs array
                    if node:
                        pair_tuple = (node.key, node.value)
                        pairs.append(pair_tuple)
                    else:
                        i += 1
            else:
                i += 1

        return pairs

    def clear(self) -> None:
        """
        Returns a cleared hash map.

        :return: removes all data from the hash and returns the empty has with the same capacity.
        """

        # create a new array (empty buckets)
        new_hash = DynamicArray()

        # appends a linked list for each index
        for i in range(self._capacity):
            new_hash.append(LinkedList())

        # set size = 0, and buckets to empty hash
        self._buckets = new_hash
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple that contains a dynamic array with the mode and frequency.

    :param da: a DynamicArray passed to the method

    :returns: a tuple with a dynamic array and integer that is the mode and frequency of da.
    """
    temp = 0
    count = 0
    high = 0

    # creates dynamic array to return
    mode_arr = DynamicArray()

    # find mode and it's frequency of da
    while temp < da.length():
        # iterates through da and calculates mode
        for i in range(da.length()):
            if da.get_at_index(temp) == da.get_at_index(i):
                count += 1
            i += 1
        # determines high and adds to array
        if count > high:
            # if count is > high, add new high to array
            high = count
            name = da.get_at_index(temp)
            if mode_arr.length() == 0:
                mode_arr.append(name)
            else:
                mode_arr = DynamicArray()
                mode_arr.append(name)
        elif count == high:
            # if count == high, adds mode to existing array
            name = da.get_at_index(temp)
            high = count
            contains = False
            for i in range(mode_arr.length()):
                if name == mode_arr.get_at_index(i):
                    contains = True

            if not contains:
                mode_arr.append(da.get_at_index(temp))
        # increases temp and resets count
        temp += 1
        count = 0

    return mode_arr, high


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
    m = HashMap(46, hash_function_1)
    m.put('key1', 10)
    m.put('key2', 11)
    m.put('key3', 15)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(9)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(46, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    m.resize_table(9)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    # m = HashMap(53, hash_function_1)
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
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
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
    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
