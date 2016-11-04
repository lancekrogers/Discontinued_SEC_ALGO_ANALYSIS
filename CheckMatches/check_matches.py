import pandas as pd

def return_matches(first_li, second_li):
    return set(first_li) & set(second_li)

def insert(df, entries):
    """
        Takes a set of values and inserts them into a dataframe sequentially where the index is
        sequential and continuous.
    """
    try:
        df.loc[max(df.index) + 1] = entries
    except ValueError:
        df.loc[0] = entries
        
def check_for_matching_phrases(df, dict1, dict2):
    '''
        This function takes in two dictionaries and checks which keys contain similar values. 
        The match percentage is found by dividing the length of the minimum set of values by 
        the matches. Always put the largest dictionary first.
    '''
    #df = pd.DataFrame(columns=['filings_name', 'no_match_name', 'percent_match'])
    for key1, value1 in dict1.items():
        for key2, value2 in dict2.items():
            matches = len(return_matches(value1, value2))
            denominator = len(max(value1, value2))
            perc_match = matches / denominator
            if perc_match >= 0.51:
                insert(df, [key1, key2, perc_match])
    return df

