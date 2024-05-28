def rgb_to_grayscale(df):
    """
    Convert RGB columns to a single grayscale column.
    """
    df['grayscale'] = 0.299 * df['red'] + 0.587 * df['green'] + 0.114 * df['blue']
    df.drop(columns=['red', 'green', 'blue'], inplace=True)
    return df
