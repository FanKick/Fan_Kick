import time

def find_fibonacci(n):
    if n <= 1:
        return n
    else:
        return find_fibonacci(n-1) + find_fibonacci(n-2)

def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

def main():
    # Inefficient Fibonacci calculation
    start_time = time.time()
    fib_result = find_fibonacci(30)
    print(f"30th Fibonacci number: {fib_result}")
    print(f"Time taken: {time.time() - start_time} seconds")

    # Inefficient list processing
    large_list = list(range(1000000))
    processed_data = process_data(large_list)
    print(f"First 5 processed items: {processed_data[:5]}")

    # Unnecessary loop
    sum_result = 0
    for i in range(1000000):
        sum_result += i
    print(f"Sum of numbers from 0 to 999999: {sum_result}")

    # Inefficient string concatenation
    long_string = ""
    for i in range(10000):
        long_string += str(i)
    print(f"Length of concatenated string: {len(long_string)}")

if __name__ == "__main__":
    main()