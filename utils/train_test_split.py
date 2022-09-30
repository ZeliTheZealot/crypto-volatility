# assumes a monotonically increasing datetimeindex 
def train_test_split(df, train_last):
    df_train = df.loc[:train_last]
    df_test = df.loc[train_last:].iloc[1:]
    return df_train, df_test