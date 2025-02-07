Are there any data quality issues present?

The first thing I like to look at is missing values across the three data sets the numbers are as follows: 
Missing Values Products:
CATEGORY_1         111
CATEGORY_2        1424
CATEGORY_3       60566
CATEGORY_4      778093
MANUFACTURER    226474
BRAND           226472
BARCODE           4025

Missing Values Transactions:
RECEIPT_ID           0
PURCHASE_DATE        0
SCAN_DATE            0
STORE_NAME           0
USER_ID              0
BARCODE           5762
FINAL_QUANTITY       0
FINAL_SALE           0

Missing Values Users:
ID                  0
CREATED_DATE        0
BIRTH_DATE       3675
STATE            4812
LANGUAGE        30508
GENDER           5892

The main issue with the these values I can see are with the barcode column in both the product and transaction data sets, this is what will be used to connect the product to the transaction as it is the primary key from the products subset. There is no way to clean or fill in this data without manual entry.
Missing a large subseet of Brand and Manufacturer values can also cause issues when trying to run any kind of specific anaylsis towards those two columns. Without those values you are unable to ensure you are capturing all the sales when sorting by a specific brand and with it being a substanial number of missing values it would make any analysis pulled on those metrics unreliable.
The other missing values when it comes to the user dataset is not as detrimental to the dataset but will affect some data credibility when it comes to grouping by gender, location, or Language but missing 5000 out of 100,000 you can still draw meaningful conclusions on those parameters.
The final issue I notice is within the transaction dataset, the Final Quanity column has values coming in as "zero" when the column type is numeric, this can be fixed with simple data cleaning setting all those values to 0.


Are there any fields that are challenging to understand?

There is no overly challenging fields, there is some confusion as to why fields have certain values in them. Such as in the transcactiosn dataset it is unclear what a 0 as final quantity represents. Is this a failed sale, a return, or just an incorrect value. It is not clear why there would be a transaction with no final sale and no final quantity.
