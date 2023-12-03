from typing import List

def get_first_digit(text: str) -> str:
    for char in text:
        if char.isdigit():
            return char
    raise ValueError("String not containing digits")

def get_calibration_values(file_path: str) -> List[int]:
    calibration_values = []
    with open(file_path, 'r') as file:
        for line in file:
            first_digit = get_first_digit(line.strip())
            last_digit = get_first_digit(line.strip()[::-1])
            value = int(first_digit+last_digit)
            calibration_values.append(value)
    return calibration_values

if __name__ == "__main__":
    input_path = "../input.txt"
    values = get_calibration_values(input_path) 
    sum_values = sum(values)
    print(f"Calibration values:\n{values}")
    print(f"\nSum: {sum_values}")