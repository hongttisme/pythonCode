def sort_indices(input_list):
    # Enumerate the list to get indices and values
    enumerated_list = list(enumerate(input_list))

    # Sort the enumerated list based on the values in descending order
    sorted_indices = sorted(enumerated_list, key=lambda x: x[1], reverse=True)

    # Extract the sorted indices
    result_indices = [index for index, _ in sorted_indices]

    return result_indices

# Example usage
numbers = [10, 5, 8, 3, 10]
sorted_indices = sort_indices(numbers)

print("Original List:", numbers)
print("Sorted Indices:", sorted_indices)