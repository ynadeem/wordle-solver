import csv
from string import ascii_uppercase

import pandas as pd

from create_letter_and_word_scores import create_letter_scores, read_data


def evaluate_list(position_list):
    if position_list == []:
        return list(ascii_uppercase)
    else:
        return position_list


def all_possible_guesses(
    guess_number,
    word_must_include_list=None,
    word_must_not_include_list=None,
    pos_one_must_include_list=None,
    pos_two_must_include_list=None,
    pos_three_must_include_list=None,
    pos_four_must_include_list=None,
    pos_five_must_include_list=None,
    pos_one_must_not_include_list=None,
    pos_two_must_not_include_list=None,
    pos_three_must_not_include_list=None,
    pos_four_must_not_include_list=None,
    pos_five_must_not_include_list=None,
):
    potential_options_list = []

    if word_must_include_list is None:
        word_must_include_list = []
    if word_must_not_include_list is None:
        word_must_not_include_list = []
    if pos_one_must_include_list is None:
        pos_one_must_include_list = evaluate_list([])
    if pos_two_must_include_list is None:
        pos_two_must_include_list = evaluate_list([])
    if pos_three_must_include_list is None:
        pos_three_must_include_list = evaluate_list([])
    if pos_four_must_include_list is None:
        pos_four_must_include_list = evaluate_list([])
    if pos_five_must_include_list is None:
        pos_five_must_include_list = evaluate_list([])

    if pos_one_must_not_include_list is None:
        pos_one_must_not_include_list = []
    if pos_two_must_not_include_list is None:
        pos_two_must_not_include_list = []
    if pos_three_must_not_include_list is None:
        pos_three_must_not_include_list = []
    if pos_four_must_not_include_list is None:
        pos_four_must_not_include_list = []
    if pos_five_must_not_include_list is None:
        pos_five_must_not_include_list = []
    with open("all_word_options.csv") as f:
        data = csv.reader(f)

        for row in data:
            if len(row) == 1:
                word = row[0]
                if (
                    word[0] in pos_one_must_include_list
                    and word[1] in pos_two_must_include_list
                    and word[2] in pos_three_must_include_list
                    and word[3] in pos_four_must_include_list
                    and word[4] in pos_five_must_include_list
                ) and (
                    word[0] not in pos_one_must_not_include_list
                    and word[1] not in pos_two_must_not_include_list
                    and word[2] not in pos_three_must_not_include_list
                    and word[3] not in pos_four_must_not_include_list
                    and word[4] not in pos_five_must_not_include_list
                ):
                    # if (
                    #     word[1] == "O"
                    #     and word[2] != "O"
                    #     and word[2] != "N"
                    #     and word[3] != "O"
                    #     and word[3] != "U"
                    #     and word[4] == "T"
                    # ):
                    split_word = list(str(word))
                    word_check_sum = 0
                    has_specific_letters_check_sum = 0

                    threshhold = len(word_must_include_list)
                    for letter in split_word:
                        if letter in word_must_not_include_list:
                            word_check_sum += 1
                            break
                    for letter in word_must_include_list:
                        if letter in word:
                            has_specific_letters_check_sum += 1
                    if (word_check_sum == 0) and (
                        has_specific_letters_check_sum == threshhold
                    ):
                        potential_options_list.append(row)

    print(
        f"For guess number {guess_number}, there are a total of {len(potential_options_list):,} possible guesses"
    )
    df_potential_options = pd.DataFrame(
        potential_options_list, columns=["potential_guesses"]
    )
    return df_potential_options


def main(df_potential_options, df_letter_scores, df_word_frequency):

    pass


if __name__ == "__main__":
    wordle_solutions_filepath = "all_word_options.csv"
    word_frequency_filepath = "word-frequency.csv"
    data = read_data(wordle_solutions_filepath, word_frequency_filepath)
    df_wordle_options = data[0]
    df_word_frequency = data[1]
    df_letter_scores = create_letter_scores(df_wordle_options)

    guess_number = 1
    word_must_include_list = ["E", "R"]
    word_must_not_include_list = ["O", "A", "S"]
    pos_one_must_include_list = None
    pos_two_must_include_list = None
    pos_three_must_include_list = None
    pos_four_must_include_list = None
    pos_five_must_include_list = None
    pos_one_must_not_include_list = None
    pos_two_must_not_include_list = ["R"]
    pos_three_must_not_include_list = None
    pos_four_must_not_include_list = None
    pos_five_must_not_include_list = ["E"]
    df_potential_options = all_possible_guesses(
        guess_number=guess_number,
        word_must_include_list=word_must_include_list,
        word_must_not_include_list=word_must_not_include_list,
        pos_one_must_include_list=pos_one_must_include_list,
        pos_two_must_include_list=pos_two_must_include_list,
        pos_three_must_include_list=pos_three_must_include_list,
        pos_four_must_include_list=pos_four_must_include_list,
        pos_five_must_include_list=pos_five_must_include_list,
        pos_one_must_not_include_list=pos_one_must_not_include_list,
        pos_two_must_not_include_list=pos_two_must_not_include_list,
        pos_three_must_not_include_list=pos_three_must_not_include_list,
        pos_four_must_not_include_list=pos_four_must_not_include_list,
        pos_five_must_not_include_list=pos_five_must_not_include_list,
    )
    main()
