from collections import Counter
from string import ascii_lowercase, ascii_uppercase

import numpy as np
import pandas as pd


def read_data(wordle_solutions_filepath, word_frequency_filepath):
    # Read in all wordle options and add letter counts
    df_wordle_options = pd.read_csv(
        "all_word_options.csv", header=None, names=["all_words"]
    )
    df_wordle_options.drop_duplicates(inplace=True)
    df_wordle_options = df_wordle_options[["all_words"]].join(
        pd.DataFrame(
            [Counter(word) for word in df_wordle_options["all_words"].str.upper()]
        )
        .reindex(list(ascii_uppercase), axis=1)
        .fillna(0)
        .astype(int)
    )
    # Read in English word corpus with frequency and add relative frequency counts
    df_word_frequency = pd.read_csv(
        "word-frequency.csv",
        header=None,
        delimiter=" ",
        names=["word_from_wikipedia", "word_count"],
    )
    total_word_count = df_word_frequency["word_count"].sum()
    df_word_frequency["word_frequency"] = (
        df_word_frequency["word_count"] / total_word_count
    )
    df_word_frequency = df_word_frequency[
        df_word_frequency["word_from_wikipedia"].str.len() == 5
    ].copy()
    df_word_frequency["word_from_wikipedia"] = df_word_frequency[
        "word_from_wikipedia"
    ].apply(lambda x: x.upper() if x.isalpha() else 0)
    df_word_frequency = pd.merge(
        df_wordle_options,
        df_word_frequency,
        how="left",
        left_on="all_words",
        right_on="word_from_wikipedia",
    )
    return [df_wordle_options, df_word_frequency]


def create_letter_scores(df):
    # Calculate with each letter only counting once
    summary_df_counts_once = (
        df[list(ascii_uppercase)].sum().to_frame(name="count_of_letter_once")
    )
    summary_df_counts_once["pct_count_once"] = (
        summary_df_counts_once["count_of_letter_once"]
        / summary_df_counts_once["count_of_letter_once"].sum()
    )
    summary_df_counts_once.reset_index(inplace=True)
    summary_df_counts_once.columns = [
        "letter",
        "count_of_letter_once",
        "pct_count_once",
    ]
    # Calculate with each letter counting as many times as it appears
    summary_df_counts_all = (
        df[list(ascii_uppercase)].sum().to_frame(name="count_of_letter_all")
    )
    summary_df_counts_all["pct_count_all"] = (
        summary_df_counts_all["count_of_letter_all"]
        / summary_df_counts_all["count_of_letter_all"].sum()
    )
    summary_df_counts_all.reset_index(inplace=True)
    summary_df_counts_all.columns = ["letter", "count_of_letter_all", "pct_count_all"]
    # Combine both scores to single dataframe
    df_letter_scores = pd.merge(
        summary_df_counts_all, summary_df_counts_once, how="inner", on="letter"
    )
    return df_letter_scores
