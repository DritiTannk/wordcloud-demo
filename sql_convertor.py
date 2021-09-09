import pandas as pd

from sqlalchemy import create_engine


if __name__ == '__main__':
    # Create sqlite engine
    engine = create_engine("sqlite:///input/sentiment_db.sqlite")
    # Read database table and creates the dataframe
    sql_df = pd.read_sql_table('Sentiment', engine, columns=['text', 'sentiment'], index_col='id')
    # Create csv file
    sql_df.to_csv('input/sentiment.csv')
    print('\n\n CSV File Created Sucessfully!')

