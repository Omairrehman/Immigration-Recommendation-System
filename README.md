# Immigration-Recommendation-System

#Problem Definition: 

The USA is considered one of the most popular countries for immigrants. Every year U.S Citizenship and Immigration Services (USCIS) receives more than 2 million applications and grants around more than 800,000 applications.  With millions of applications coming up every year and immigrants continuing to find their past ethnic identification in the neighborhoods with the focus for acculturation to urban life, it’s becoming a challenge for immigration applicants to choose a place to settle in. Our team sees a clear need for an easier way to visualize a map based on past ethnic concentration of a specific nationality that will make the decision of choosing a state for an immigrant easier along with assessing personal security in a state. 

# Proposed Solution: 

We are planning to develop a flask application which will allow the users to choose which nationality they identify with and based on their selection we will show the states where people with the same nationality have settled in. We have chosen the datasets provided by Homeland Security to map out the concentrations of each immigrant’s nationality in the U.S and a dataset provided by FBI on hate crimes to assess personal security risks in each state. We will build an application that will recommend potential immigrants which states in the US are preferable for them to settle based on their nationality and hate crime rating. 

#Data Collection
We have collected data on the number of permanent residency/green card issued from 2007 to 2019 for about 200 countries, broken down at state-level as well as county-level, from the department of homeland security. Furthermore, we are using open data soft website to get the data set on the geolocation points of the counties.  And we have also collected data on the number of hate crimes reported at a state-level from 2007 to 2019 from the FBI's Uniform Crime Reporting (UCR) Program's hate crime statistics datasets.

For hatecrime dataset we first downloaded xls files from the website and then manually cleaned it by getting rid of unncessary headers and converted into csvs on Microsoft Excel.

For geopoints dataset after downloading it as xls file (as csv file was corrupted) from the website we got rid of unncessary columns manually because it was giving errors and then we converted into CSV for the columns we needed.

LPR Admissions data: https://www.dhs.gov/immigration-statistics/readingroom/LPR/LPRcounty
Hate Crime data: https://ucr.fbi.gov/hate-crime/2018/topic-pages/tables/table-11.xls
Geopoints data: https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name

#Data Transformation
We worked on google colab on ipnyb notebooks to clean and transform our data to use it for our proposed solution. 

We extracted the data from the collected csvs and then cleaned it. After cleaning we merged the three different datasets into one (result_dataframe)  

In our application, number of hate crimes are given along with a hate crime rating. Hate crimes are recorded from 2007 to 2019 for each state. A hate crime index was created as a ratio of total hate crimes happening in a state to  total number of admissions of immigrants in each state over the same time period. Statistical analysis showed the following quartiles of the crime index:
First Quartile (25%):  0.006783 hatecrime per admission (2007-2019)
Second Quartile (50%):  0.006783 to 0.019142 hatecrime per admission (2007-2019)
Third Quartile (75%): 0.019142 to 0.039815 hatecrime per admission (2007-2019)
Fourth Quartile (100%):  above 0.039815 hatecrime per admission (2007-2019)

If the value was below first quartile the rating will be “Very Low” while if it’s within the second quartile then rating will be “Low”. On the other hand, if the value of crime index comes within third or fourth quartile then the rating will be “High” and “Very High” respectively. 

A hate crime rating is necessary as it helps the user to understand what hate crime numbers indicate.

#Data Load 
After transforming the data, we exported a Csv (working_finale.csv) which was used to get data and import it into Flask app. 
After that within flask app we used html forms to collect userinput which to choose their country of birth and also number of recommendations they want to see on the map. After that data is submitted through POST method it leads the user to another page where that recommended map is displayed with the number of recommendations they wanted. We used the variable limit to create a new user dataframe after comparing the chosen country of birth with the working finale's Country of Birth which essentially filters the dataframe accordingly and then truncate it to the limit provided. Sorting by total admissions is used to recommend the most concentrated/popular destinations to the user by getting the descending order. Bokeh and google map API is used to display the data on the map. 

#Front End
For front end purposes, Google fonts, paletton, bootstrap and customized css is used to make the visual experience appealing for the user. Since we are promising our users easier access to accurate information we've chosen the color blue for our website as it's linked with trust and loyalty. After researching more about blue color theory we found out that is also associated with tranquility and calmness. Thus reassuring our users of the correct information given. Paletton was used to create the monochromatic color theme for our website. Moreover, an About page is also linked with our application so that the users can research about our mission statement, the methodology we used to create hate crime ratings and all the data collection. We've also included our bios and photos to humanize the application for the user.  