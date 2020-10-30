import re
import numpy as np
from numexpr import evaluate


def arithmetic_arranger(problems, answers=False):

    def validation(prob_list):  # checks that problems are valid
        # checks that number of problems does not exceed 5
        if len(prob_list) > 5:
            return "Error: Too many problems."

        # joins problems into a single string for easy regex parsing
        joined_problems = " ".join(problems)

        # checks problems for multiplication or division
        if re.search("[*/]", joined_problems):
            return "Error: Operator must be '+' or '-'."

        # checks problems for alphabetic characters
        if re.search("[A-Za-z]", joined_problems):
            return "Error: Numbers must only contain digits."

        # checks problems for operands greater than four digits
        for operand in re.findall("\d+", joined_problems):
            if len(operand) > 4:
                return "Error: Numbers cannot be more than four digits."

        return "OK"

    def processing(expression):  # create arrays containing formatted problems
        # evaluates solution
        solution = str(evaluate(expression))

        # splits problem on whitespace
        split_expression = expression.split(sep=" ")

        # extracts operator from split_expression
        operator = split_expression.pop(1)

        # determines length of formatting array
        array_length = len(max(split_expression, key=len)) + 2

        # determines height of formatting array based on value of answers
        if answers:
            format_array = np.empty([4, array_length], dtype=str)
        else:
            format_array = np.empty([3, array_length], dtype=str)

        # inserts terms into array
        for rownum in range(2):
            term = split_expression[rownum]
            for index, digit in enumerate(term[::-1]):
                format_array[rownum, -(index + 1)] = digit

        # inserts operator into array
        format_array[1, 0] = operator

        # inserts dashes into array
        for index in range(len(format_array[2])):
            format_array[2, index] = "-"

        # inserts answers into array if applicable
        try:
            format_array[3]
        except IndexError:
            pass
        else:
            for index, digit in enumerate(solution[::-1]):
                format_array[3, -(index + 1)] = digit

        return format_array

    def merge_formatted(arrays):  # merges formatted problem arrays
        merged_array = None
        space_array = np.empty([arrays[0].shape[0], 4], dtype=str)
        for index, array in enumerate(arrays):
            if index == 0:
                merged_array = array
            else:
                merged_array = np.hstack((merged_array, space_array))
                merged_array = np.hstack((merged_array, array))
        return merged_array

    def print_problems(merged_array):  # prints formatted problems to the variable print_string
        print_string = ""
        for index, row in enumerate(merged_array):
            for element in row:
                if str(element):
                    print_string += element
                else:
                    print_string += " "
            if index < len(merged_array) - 1:
                print_string += "\n"
        return print_string

    def main():
        validation_result = validation(problems)
        if validation_result == "OK":
            arrays = []
            for problem in problems:
                arrays.append(processing(problem))
            merged_array = merge_formatted(arrays)

            return print_problems(merged_array)
        else:
            return validation_result

    return main()
