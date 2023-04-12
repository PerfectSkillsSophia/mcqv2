from thefuzz import fuzz, process
from langdetect import detect
import re


def Cal_Accu(s1, s2):
    Percent_ratio = 0
    checker = ""
    z = re.split(r'[ ,.!;"]', s1)
    for i in z:
        if len(i) == 1:
            checker = i

    x = re.split(r'[ ,.!;"]', s2)

    if len(x) == 1:
        if checker.lower() == s2.lower():
            Percent_ratio = 100
        return Percent_ratio

    else:
        count = 0
        last = ""
        check = 0
        if "Correct" in x or "correct" in x:
            for i in x:
                if check == 0 and len(i) == 1:
                    last = i
                    count = 3
                if "Correct" == i or "correct" == i:
                    check = 1

                if len(i) == 1 and check == 1:
                    if checker.lower() == i.lower():
                        Percent_ratio = 100
                    return Percent_ratio
                count -= 1

        if checker.lower() == last.lower() and count == 1:
            Percent_ratio = 100
            return Percent_ratio

    # Accuracy Calculation Method Starts
    lang = detect(s2)

    if (lang == "en") or (
        s2 == "a"
        or s2 == "A"
        or s2 == "b"
        or s2 == "B"
        or s2 == "c"
        or s2 == "C"
        or s2 == "d"
        or s2 == "D"
    ):
        if fuzz.partial_token_sort_ratio(s1, s2) == 100:
            Percent_ratio = 100
        elif (
            fuzz.partial_token_sort_ratio(s1, s2) != 100
            and fuzz.token_sort_ratio(s1, s2) != 100
            and fuzz.token_set_ratio(s1, s2) != 100
            and fuzz.partial_ratio(s1, s2) != 100
        ):
            Percent_ratio = max(
                fuzz.partial_token_sort_ratio(s1, s2),
                fuzz.token_sort_ratio(s1, s2),
                fuzz.token_set_ratio(s1, s2),
                fuzz.partial_ratio(s1, s2),
            )
        else:
            Percent_ratio = (
                (
                    fuzz.partial_token_sort_ratio(s1, s2)
                    + fuzz.token_sort_ratio(s1, s2)
                    + fuzz.token_set_ratio(s1, s2)
                    + fuzz.partial_ratio(s1, s2)
                )
                / 400
            ) * 100
    return Percent_ratio


# Accuracy Calculation Method Ends


# Test Cases
# S1 is predefined answer
# S2 is expected answer


# Test Case 1
# S1 = "c"
# S2 = "option c"
# Accuracy 100%

# Test Case 2
# S1 = "c"
# S2 = "option b"
# Accuracy 0%

# Test Case 3
# S1 = "c"
# S2 = "c option"
# Accuracy 100%

# Test Case 4
# S1 = "c"
# S2 = "a option"
# Accuracy 0%

# Test Case 5
# S1 = "c"
# S2 = "a correct answer is c"
# Accuracy 100%

# Test Case 6
# S1 = "c"
# S2 = "a correct answer is d"
# Accuracy 0%