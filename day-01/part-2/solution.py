from typing import List
import numpy as np


def get_first_last_digits(line: str) -> str:
    word_digits = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    digit_word = {value: key for key, value in word_digits.items()}
    
    # substitute digit with word digits
    for char in line:
        if char.isdigit():
            line = line.replace(char, digit_word[char])
    
    # first word digit
    word_digit_idx = [line.find(word) for word in word_digits.keys()]
    word_digit_idx = np.array([idx if idx >=0 else np.nan for idx in word_digit_idx])
    first_word_digit = int(np.nanargmin(word_digit_idx))

    # last word digit
    word_digit_idx = [line.rfind(word) for word in word_digits.keys()]
    word_digit_idx = np.array([idx if idx >=0 else np.nan for idx in word_digit_idx])
    last_word_digit = int(np.nanargmax(word_digit_idx))
    
    return int(f"{first_word_digit}{last_word_digit}")
        

def get_calibration_values(file_path: str) -> List[int]:
    calibration_values = []
    with open(file_path, 'r') as file:
        for line in file:
            value = get_first_last_digits(line.strip())
            calibration_values.append(value)
    return calibration_values

if __name__ == "__main__":
    input_path = "../input.txt"
    values = get_calibration_values(input_path) 
    sum_values = sum(values)
    print(f"Calibration values:\n{values}")
    print(f"\nSum: {sum_values}")