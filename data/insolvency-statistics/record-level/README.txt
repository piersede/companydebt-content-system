The accompanying file contains a list of insolvencies registered in England, Wales and Scotland between 1 January 2012 and 30 April 2024. They are based on data from Insolvency Service administrative systems for compulsory liquidations in England and Wales, and on Companies House data for all other insolvencies. In addition to the dataset, there is a metadata file to explain what each column contains.

Information on SIC codes can be found on the Office for National Statistics website at https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2007

The dataset contains bulk insolvencies. For more details on bulk insolvencies, see the glossary in the main data tables of the most recent monthly statisitcs at https://www.gov.uk/government/statistics/company-insolvency-statistics-april-2024. For most measures of insolvency, we recommend filtering out cases where the Bulk variable is "Y".

The dataset contains CVLs directly following administrations. Companies that go through this process will therefore be included twice in these statistics, so when counting the number of companies entering insolvency in a given period, we recommend filtering out cases where the type variable is "Administration to CVL".

To reproduce the data used for the April publication tables (https://www.gov.uk/government/statistics/company-insolvency-statistics-april-2024), filter for month registered not equal to months between 2012-01 and 2013-12 and use the following filters on the dataset:
Table 1b - Number of insolvencies in England and Wales: isBulk = "N", register.location = "England/Wales", type does not equal "Administration to CVL" or "Moratorium"
Table 1d - Number of insolvencies in England and Wales, including bulk insolvencies: isBulk = "Y", register.location = "England/Wales", type does not equal "Administration to CVL" or "Moratorium"
Table 2 - Number of administration to CVLs: register.location = "England/Wales", type = "Administration to CVL"
Table 4 - Number of insolvencies in Scotland: register.location = "Scotland", type does not equal "Administration to CVL"
Table 1c and the quarterly industry tables - filter by SIC 1-, 2-, 3-, 4- or 5- digit code, register location and insolvency type as required, isBulk = "N", type does not equal "Administration to CVL" 

Note that information to 5-digit level is not available for some companies. SIC information is more reliable for 1-digit sectors than lower level breakdowns.

Tables 3 and 5 can be reproduced using the data for Tables 1b and 4 above, along with the active register size information provided in Companies House official statistics. Record-level information on insolvency in Northern Ireland as presented in Tables 6 and 7 is currently unavailable.

If you have any questions, or require support on using this dataset, please contact statistics@insolvency.gov.uk

This data is provided for statistical purposes only. We can not guarantee that it is free from error and therefore should not be used to determine whether a particular company is insolvent.