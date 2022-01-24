import csv

potential_options_list = []
with open("all_word_options.csv") as f:
    data = csv.reader(f)
    for row in data:
        if len(row) == 1:
            word = row[0]
            if word[1] == "N" and word[2] == "O" and word[3] != "N" and word[4] != "N":
                split_word = list(str(word))
                word_check_sum = 0
                has_specific_letters_check_sum = 0
                must_include_list = ["O", "N", "L"]
                must_not_include_list = [
                    "W",
                    "E",
                    "R",
                    "T",
                    "U",
                    "I",
                    "A",
                    "D",
                    "H",
                    "C",
                ]
                threshhold = len(must_include_list)
                for letter in split_word:
                    if letter in must_not_include_list:
                        word_check_sum += 1
                        break
                for letter in must_include_list:
                    if letter in word:
                        has_specific_letters_check_sum += 1
                if (word_check_sum == 0) and (
                    has_specific_letters_check_sum == threshhold
                ):
                    potential_options_list.append(row)

print(potential_options_list)
