import math

class Node:
    def __init__(self):
        self.tag = -1
        self.block = 0
        self.valid = 0

    @staticmethod
    def print_binary(num, n):
        binary_str = "{0:b}".format(num).zfill(n)
        print(binary_str, end='\t\t')

    @staticmethod
    def display(cache, lines, tag_bits):
        print("Index ValidBit Tag \t\t Data(decimal)")
        for i in range(lines):
            if cache[i].tag != -1:
                print(f"{i} \t {cache[i].valid} \t", end='')
                Node.print_binary(cache[i].tag, tag_bits)
                print(f" Block {cache[i].block}")
            else:
                print(f"{i} \t {cache[i].valid} \t -- \t\t\t {cache[i].block}")

def direct_mapping(cache, ref, offset_bits, index_bits, tag_bits, hit, miss, replacements):
    offset = ref & ((1 << offset_bits) - 1)
    temp = ref >> offset_bits
    index = temp & ((1 << index_bits) - 1)
    tag = temp >> index_bits

    print("\nINSTRUCTION BREAKDOWN\n")
    print(f"Tag \t\tIndex \t\tOffset \n{tag} \t\t{index} \t\t{offset}")
    Node.print_binary(tag, tag_bits)
    Node.print_binary(index, index_bits)
    Node.print_binary(offset, offset_bits)
    print("\n")
    print(f"{tag_bits} bits \t\t{index_bits} bits \t\t{offset_bits} bits")
    if cache[index].valid == 0:
        print("Miss")
        miss[0] += 1
        cache[index].tag = tag
        cache[index].valid = 1
        cache[index].block = temp
    else:
        if cache[index].tag != tag:
            print("Miss")
            miss[0] += 1
            replacements[0] += 1
            cache[index].tag = tag
            cache[index].block = temp
        else:
            print("Hit")
            hit[0] += 1

def is_power_of_two(n):
    return (n & (n - 1)) == 0 and n != 0

if __name__ == "__main__":
    hit = [0]
    miss = [0]
    replacements = [0]
    mem_size = int(input("Main memory size is: "))
    while mem_size <= 0 or not is_power_of_two(mem_size):
        print("Please enter a positive integer which is a power of 2!")
        mem_size = int(input("Main memory size is: "))
    cache_size = int(input("Cache memory size is: "))
    while cache_size <= 0 or not is_power_of_two(cache_size):
        print("Please enter a positive integer which is a power of 2!")
        cache_size = int(input("Cache memory size is: "))
    block_size = int(input("Size of block is: "))
    while block_size <= 0 or not is_power_of_two(block_size):
        print("Please enter a positive integer which is a power of 2!")
        block_size = int(input("Size of block is: "))
    lines = cache_size // block_size
    cache = [Node() for _ in range(lines)]
    offset_bits = int(math.log2(block_size))
    index_bits = int(math.log2(lines))
    tag_bits = int(math.log2(mem_size) - offset_bits - index_bits)
    print("CACHE TABLE")
    Node.display(cache, lines, tag_bits)

    while True:
        ref = int(input("\nMain memory address in decimal is (-1 to exit): "))
        if ref == -1:
            break
        direct_mapping(cache, ref, offset_bits, index_bits, tag_bits, hit, miss, replacements)
        print("\n\nCACHE TABLE")
        Node.display(cache, lines, tag_bits)
        total = hit[0] + miss[0]
        hit_ratio = (hit[0] / total) * 100 if total > 0 else 0
        miss_ratio = (miss[0] / total) * 100 if total > 0 else 0
        print(f"Total hits: {hit[0]} Total misses: {miss[0]}")
        print(f"Replacements: {replacements[0]}")
        print(f"Hit ratio: {hit_ratio:.2f}% Miss ratio: {miss_ratio:.2f}%")
