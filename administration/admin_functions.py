from thefuzz import fuzz
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

        if checker.lower() == last.lower():
            Percent_ratio = 100
        else:
            Percent_ratio = 0
            return Percent_ratio
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
