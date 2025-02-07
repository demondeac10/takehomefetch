# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 10:09:02 2025

@author: brenn
"""

import pandas as pd
from datetime import datetime as dt
from os.path import basename
import os, re, time

def main():
        ## First step is to read in all the datasets into dataframes       
        product_df = pd.read_csv(r"C:\Users\brenn\Downloads\PRODUCTS_TAKEHOME.csv")
        transaction_df = pd.read_csv(r"C:\Users\brenn\Downloads\TRANSACTION_TAKEHOME.csv")
        user_df = pd.read_csv(r"C:\Users\brenn\Downloads\USER_TAKEHOME.csv")
        
        ##These three sets of codes are checking for null values across the three csv files and giving an idea on how much data we are missing
        missing_values_product = product_df.isnull().sum()
        print("Missing Values Products:")
        print(missing_values_product)
        
        missing_values_transaction = transaction_df.isnull().sum()
        print("Missing Values Transactions:")
        print(missing_values_transaction)
        
        missing_values_user = user_df.isnull().sum()
        print("Missing Values Users:")
        print(missing_values_user)
      
        ##Create dataframe with Transactions and users merged using left to ensure only those with transactions are included
        merged_df = transaction_df.merge(user_df, left_on="USER_ID", right_on="ID", how="left")
        ##Merge another dataframe to include the product data
        final_merged_df = merged_df.merge(product_df, left_on="BARCODE", right_on="BARCODE", how="left")
    
        
        ##Get current date to calculate age of the users
        current_date = dt.now()
        
        ##Have to add in a few lines to convert column types to datetime
        final_merged_df["BIRTH_DATE"] = pd.to_datetime(final_merged_df["BIRTH_DATE"], errors='coerce')
        final_merged_df["CREATED_DATE"] = pd.to_datetime(final_merged_df["CREATED_DATE"], errors='coerce')
        final_merged_df["PURCHASE_DATE"] = pd.to_datetime(final_merged_df["PURCHASE_DATE"], errors='coerce')
        
        ##Fixing issues with timezones causing issues calcuationg the Account Age, and Age of person
        final_merged_df["BIRTH_DATE"] = final_merged_df["BIRTH_DATE"].dt.tz_localize(None)
        final_merged_df["CREATED_DATE"] = final_merged_df["CREATED_DATE"].dt.tz_localize(None)
        final_merged_df["PURCHASE_DATE"] = final_merged_df["PURCHASE_DATE"].dt.tz_localize(None)
        
        ##Get current date to calculate age of the users
        final_merged_df["AGE"] = final_merged_df["BIRTH_DATE"].apply(lambda x: (current_date - x).days // 365 if pd.notnull(x) else None)
        final_merged_df["ACCOUNT_AGE"] = final_merged_df["CREATED_DATE"].apply(lambda x: (current_date - x).days if pd.notnull(x) else None)

        ##Create a new Dataframe of only over 21 users
        over_21 = final_merged_df[final_merged_df["AGE"] >= 21]
        ##Get count of the values for each brand name
        top_brands_21 = over_21["BRAND"].value_counts().head(5)
        
        print(top_brands_21)
        
        ##Create a new dataframe of accounts over 180 days
        old_accounts = final_merged_df[final_merged_df["ACCOUNT_AGE"] >= 180]
        ##Converting final sale column to numeric to standardize data in the column
        old_accounts["FINAL_SALE"] = pd.to_numeric(old_accounts["FINAL_SALE"], errors='coerce')
        ##Group the sales by store name to get the largest brand sales for the dataframe containing accounts over 180 days
        brand_sales = old_accounts.groupby("STORE_NAME")["FINAL_SALE"].sum().nlargest(5)
        
        print(brand_sales)
        
        ##Fix datetime column
        user_df["CREATED_DATE"] = pd.to_datetime(user_df["CREATED_DATE"], errors='coerce')
        ##Get only the year from the column to easily group and run calcuations on
        user_df["YEAR_CREATED"] = user_df["CREATED_DATE"].dt.year
        ##Get number of users created in each year
        yearly_user_growth = user_df["YEAR_CREATED"].value_counts().sort_index()
        ##Calcualte the percent change over year and convert to a percentage
        yoy_growth = yearly_user_growth.pct_change() * 100
        
        print(yoy_growth)
        
if __name__ == '__main__':
    main()