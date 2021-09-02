# Factors-that-correlate-to-the-spread-of-COVID-19

### Quick Overview of the files and folders

Factors that correlate to the spread of COVID-19.rmd: The R code used to produce the graphs and do analysis. 

Factors that correlate to the spread of COVID-19.html: The knit html file that the R code produces.  

preprocessing.py: Python program used to filter countries and process the raw csvs into a large csv that the R program could digest. 

processed data (folder): The processed data that preprocessing.py generated. 

Data processing: The raw csvs downloaded from ourworldindata.org. 

raw data.zip: The raw csvs in a zip file. 

report.pdf: The final report that explains all the data, methodologies, statistical methods, graphs, and analysis.  

### Project Setup

This is a project aimed at using regression to find out which factors explain the spread of COVID-19 in countries.
Which countries were successful at preventing the spread, which countries were less successful, and why?
The "success" of a country is defined by both deaths due to, and cases of, COVID-19 per million people.
<br/><br/>
All data is from https://ourworldindata.org/charts, and 15 variables have been chosen.  
Those under the category of demographics and economy are: population density, population, GDP per capita, median age, urbanization, and life expectancy.  
Those under the category of health are: respiratory disease death rate, physicians per 100 people, and health expenditure per capita.  
Those under the category of COVID-19 response policy are: contact tracing, international travel controls, stay-at-home requirements, public gathering restrictions,
internal movement restrictions, and test per million people.
A more detailed explanation of how the data is defined can be found in report.pdf.  

An important note is that out of the 200 or so countries in the world, only about 100 ended up being considered for analysis.
This is because data was not available for many of the countries in ourworldindata.org, and the reasoning and details of how these decisions were made can be found in report.pdf.  

The csv sheets from ourworldindata.org needed to be merged into a single csv that could be easily read by R,
and a description of how the data was processed can be found in preprocessing.py.  

### Data analysis and conclusions

Long story short, a traditional MLR did not work well (see report.pdf for details). A GAM (generalized additive model) was used instead, with perceivable improvements.  
The summary of findings can be found in report.pdf in the "Data Analysis: Comparing Models and Variables with a Table" section.  

To summarize, the variables that had significant correlation with "cases per million people" were: population density, median age, international travel controls,
physicians per 1000 people, healthcare spenditure per capita, stay home requirements, and tests per million people. Percent urbanization and population were almost significant.  

The variables that had significant correlation with "deaths per million people" were the same variables that had correlation with "cases per million people", but
with the exceptions of: Tests per million people, percent urbanization, and population not being significant at all, along with GDP per capita being almost significant.  

The graphs of the GAM for the significant variables can be seen in Factors-that-correlate-to-the-spread-of-COVID-19.html. 
Detailed descriptions of interpretations for how the variables are significant in real life can be found in report.pdf in the "Data Analysis: Interpretations and Insights" section.
