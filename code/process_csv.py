# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

file1_path = '/home/szu/PycharmProjects/Navajoa/data/不同企业在1991-1995年间的贷款收益率.csv'
file2_path = '/home/szu/PycharmProjects/Navajoa/data/不同企业在1996-2000年间的贷款收益率.csv'
file3_path = '/home/szu/PycharmProjects/Navajoa/data/不同企业在2001-2005年间的贷款收益率.csv'

file_loan_path = '/home/szu/PycharmProjects/Navajoa/data/贷款企业一览表.csv'

df_loan_term = pd.read_csv(file_loan_path)
loan_term = list(df_loan_term.iloc[0])[1:]

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df3 = pd.read_csv(file3_path)


def del_term(df, loan_term):
    for index, i in enumerate( loan_term):
        df.replace(df.iloc[index][i + 1:], 0, inplace=True)
    return df


def get_df_year(col, df1, df2, df3):
    df_year = pd.DataFrame()
    # for i in range(num):
    df_year['{col_name}_1'.format(col_name=col)] = df1[col]
    df_year['{col_name}_2'.format(col_name=col)] = df2[col]
    df_year['{col_name}_3'.format(col_name=col)] = df3[col]
    return df_year


def get_mean_std(df_year, i):
    df = pd.DataFrame(columns=['{}mean'.format(i), '{}std'.format(i)])
    df['{}mean'.format(i)] = np.mean(df_year, axis=1)
    df['{}std'.format(i)] = np.std(df_year, axis=1)
    return df


if __name__ == '__main__':
    df1 = del_term(df1, loan_term)
    df2 = del_term(df2, loan_term)
    df3 = del_term(df3, loan_term)
    print(df1)

    df_1year = get_df_year('1年期', df1, df2, df3)
    df_2year = get_df_year('2年期', df1, df2, df3)
    df_3year = get_df_year('3年期', df1, df2, df3)
    df_4year = get_df_year('4年期', df1, df2, df3)
    df_5year = get_df_year('5年期', df1, df2, df3)

    df_1 = get_mean_std(df_1year, 1)
    df_2 = get_mean_std(df_2year, 2)
    df_3 = get_mean_std(df_3year, 3)
    df_4 = get_mean_std(df_4year, 4)
    df_5 = get_mean_std(df_5year, 5)

    df_result = pd.DataFrame()
    df_result = pd.concat([df_1, df_2, df_3, df_4, df_5], axis=1)
    print(df_result)
    df_result.to_csv('/home/szu/PycharmProjects/Navajoa/results/result_3.csv')
