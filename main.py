task_description = """ There is an array (where the order of elements does not matter) containing random integers (1...300).
The number of integers in the array is up to 1000.

Write a serialization/deserialization function to a string so that the resulting string is compact.
The goal of the task is to compress data as much as possible with relatively simple serialization without a compression algorithm (at least 50% on average).
The serialized string must contain only ASCII characters.
You can use any programming language.
Along with the solution, you need to send a set of tests - the source string, the compressed string, and the compression ratio.

Test examples: 
- The simplest short, random - 50 numbers, 100 numbers, 500 numbers, 1000 numbers
- Boundary - all numbers of 1 character, all numbers of 2 characters, all numbers of 3 characters
- Each number appearing 3 times - a total of 900 numbers.
"""

import random
from collections import Counter

value_range = (1, 300)

# Generate an array of random integers within a specified range
def generate_random_array(num_elements, value_range=value_range):
    return [random.randint(value_range[0], value_range[1]) for _ in range(num_elements)]

# Generate a sequential array from start to end
def generate_sequential_array(start, end):
    return list(range(start, end + 1))

# Serialize an array to a string with semicolon delimiters
def simple_serialize(array):
    """
    This is the baseline serialization method. The average length of an element 
    for random integers in the range (1, 300) is approximately 2.64 characters 
    (calculated as (9*1 + 90*2 + 201*3) / 300). Adding a separator between elements 
    increases the average length per element to roughly 3.64 characters.
    """
    return ';'.join(map(str, array))


# Deserialize a string back to an array of integers
def simple_deserialize(s):
    return list(map(int, s.split(';')))

# Validate that two arrays have the same elements
def validate_arrays(original, deserialized):
    return Counter(original) == Counter(deserialized)


# Serialize an array using delta encoding
def delta_serialize(array):
    """
    I decided to use delta encoding because the order of elements in the array is not important,
    allowing the array to be sorted. For arrays whose size is comparable to the range of random numbers,
    the differences between numbers after sorting are often single digits. As the array size increases
    relative to the random number range, it becomes more likely that delta encoding will result in all
    elements being single digits.
    
    Instead of using separators for each element in the delta array, which would almost double the
    average element length from ~1 character to ~2, I chose to encode the string so that an element is
    assumed to be 1 character unless otherwise indicated. Two-digit elements are prefixed with one
    tilde (~), and three-digit elements with two tildes. Wrapping multi-character numbers in special
    symbols would logically require two additional characters for each multi-character number, but my
    implementation achieves this with only one.
    
    Using delta encoding alone is generally sufficient to achieve at least 50% compression on average,
    as required by the task.
    """
    if not array:
        return ""
    
    sorted_array = sorted(array)  # Sort the array for bests results from delta encoding
    deltas = [sorted_array[0]] + [sorted_array[i] - sorted_array[i - 1] for i in range(1, len(sorted_array))]  # Compute deltas
    
    serialized = ""
    for delta in deltas:
        delta_str = str(delta)
        serialized += '~' * (len(delta_str) - 1) + delta_str  # Encode deltas with tilde prefixes for multi-character numbers
    
    return serialized

# Deserialize a string back to an array using delta decoding
def delta_deserialize(s):
    if not s:
        return []
    
    numbers = []
    current_number = ""
    i = 0
    while i < len(s):
        if s[i] == '~':  # Detect multi-character number prefix
            tilde_count = 1
            while i + 1 < len(s) and s[i + 1] == '~':
                tilde_count += 1
                i += 1
            i += 1
            number_length = tilde_count + 1
            current_number = s[i:i + number_length]  # Extract multi-character number
            i += number_length - 1
        else:
            current_number = s[i]  # Single character number
        
        numbers.append(int(current_number))
        i += 1
    
    if numbers:
        original_values = [numbers[0]]  # Initialize the first value
        for i in range(1, len(numbers)):
            original_values.append(original_values[-1] + numbers[i])  # Reconstruct original values using deltas
    
    return original_values


# Compress a string using a custom Base91 encoding
def baseX_to_base91(input_string):
    """
    I decided to complicate the code by adding this non-trivial function for several reasons: 
    First, it's fun. 
    Second, the task required maximum compression and allowed the use of all printable ASCII
    characters.
    
    For maximum efficiency, the string can be interpreted as a number in BaseX and converted to a
    number in BaseY. The greater the difference between X and Y, the shorter the resulting string. I
    decided to determine X by the number of unique characters in the string. Using Base10 for storing
    "20216022" is wasteful since Base4 with the dictionary "0216" is sufficient.
    
    As for BaseY, I could have used the popular Base64, but there are more printable ASCII characters,
    and we were allowed to use them all. Hence, I used the maximum, excluding only ' " and ~. The BaseX
    dictionary is placed at the beginning of the string - it occupies very little space compared to the
    compression it achieves.
    """
    base91_dict = " !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}"
    base91_base = len(base91_dict)
    
    unique_chars = sorted(set(input_string))
    if len(unique_chars) == 1:
        unique_chars.insert(0, "~")  # Ensure there are at least two unique characters
    custom_base = len(unique_chars)
    
    if input_string[0] == unique_chars[0]:
        unique_chars.append(unique_chars.pop(0))  # Move first unique char to end to avoid leading zeroes loss
    
    char_to_value = {char: idx for idx, char in enumerate(unique_chars)}

    base10_value = 0
    for i, char in enumerate(reversed(input_string)):
        # Using Base10 as an intermediary simplifies conversion and ensures accuracy
        base10_value += char_to_value[char] * (custom_base ** i)  # Convert BaseX to Base10
    
    base91_value = []
    while base10_value > 0:
        remainder = base10_value % base91_base
        base91_value.append(base91_dict[remainder])  # Convert Base10 to Base91
        base10_value //= base91_base
    base91_value.reverse()
    
    return ''.join(unique_chars) + '~' + ''.join(base91_value)  # Combine BaseX dictionary with Base91 encoded value

# Decompress a Base91 encoded string back to the original string
def base91_to_baseX(formatted_string):
    """
    This function reverses the process done in baseX_to_base91.
    It decodes a Base91 encoded string back to the original string using the BaseX dictionary.
    """
    base91_dict = " !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}"
    base91_base = len(base91_dict)
    
    split_index = formatted_string.rfind('~')
    dictionary = formatted_string[:split_index]  # Extract the BaseX dictionary
    base91_encoded = formatted_string[split_index + 1:]
    
    base10_value = 0
    for i, char in enumerate(reversed(base91_encoded)):
        # Once again, using Base10 as an intermediary to avoid unobvious errors
        base10_value += base91_dict.index(char) * (base91_base ** i)  # Convert Base91 to Base10
    
    custom_base = len(dictionary)
    value_to_char = {idx: char for idx, char in enumerate(dictionary)}
    original_chars = []
    while base10_value > 0:
        remainder = base10_value % custom_base
        original_chars.append(value_to_char[remainder])  # Convert Base10 to BaseX using dictionary
        base10_value //= custom_base
    original_chars.reverse()
    
    return ''.join(original_chars)  # Return the decompressed original string


# Define test cases as requested in the task description
test_cases = {
    "Random 50": generate_random_array(50),
    "Random 100": generate_random_array(100),
    "Random 500": generate_random_array(500),
    "Random 1000": generate_random_array(1000),

    "Random 50 One Digit": generate_random_array(50, (1,9)),
    "Random 100 One Digit": generate_random_array(100, (1,9)),
    "Random 500 One Digit": generate_random_array(500, (1,9)),
    "Random 1000 One Digit": generate_random_array(1000, (1,9)),

    "Random 50 Two Digit": generate_random_array(50, (10,99)),
    "Random 100 Two Digit": generate_random_array(100, (10,99)),
    "Random 500 Two Digit": generate_random_array(500, (10,99)),
    "Random 1000 Two Digit": generate_random_array(1000, (10,99)),

    "Random 50 Three Digit": generate_random_array(50, (100,300)),
    "Random 100 Three Digit": generate_random_array(100, (100,300)),
    "Random 500 Three Digit": generate_random_array(500, (100,300)),
    "Random 1000 Three Digit": generate_random_array(1000, (100,300)),

    "One Digit Sequential": generate_sequential_array(1, 9),
    "Two Digit Sequential": generate_sequential_array(10, 99),
    "Three Digit Sequential": generate_sequential_array(100, 300),
    
    "Three of Each": [i for i in range(1, 301) for _ in range(3)]
}
# Test the compression and decompression process
def test_compression(array):
    original = simple_serialize(array)  # Baseline serialization
    serialized_delta = delta_serialize(array)  # Delta encoding
    compressed_base91 = baseX_to_base91(serialized_delta)  # Base91 compression
    decompressed_base91 = base91_to_baseX(compressed_base91)  # Decompress Base91
    deserialized_array = delta_deserialize(decompressed_base91)  # Delta decoding
    
    original_length = len(original)
    compressed_length = len(compressed_base91)
    compression_ratio = original_length / compressed_length if compressed_length != 0 else float('inf')  # Calculate compression ratio
    
    is_valid = validate_arrays(array, deserialized_array)  # Validate if original and deserialized arrays are equal
    
    return {
        "original": original,
        "serialized_delta": serialized_delta,
        "compressed": compressed_base91,
        "original_length": original_length,
        "compressed_length": compressed_length,
        "compression_ratio": compression_ratio,
        "validity": is_valid
    }


# Run tests on each test case
for test_name, array in test_cases.items():
    result = test_compression(array)
    print(f"""Test Case: {test_name}
Baseline serialization: {result['original']}
First step, delta serialization: {result['serialized_delta']}
Second step, Base91 compression: {result['compressed']}
Original Length: {result['original_length']}
Compressed Length: {result['compressed_length']}
Compression Ratio: {result['compression_ratio']:.2f}
Validity: {'Valid' if result['validity'] else 'Invalid'}
{"-" * 30}""")

