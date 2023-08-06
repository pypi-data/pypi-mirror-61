# Handle-Missing-Values 
Create and save .csv file with replaced categorical and non-categorical missing values
<H2>Brief</H2>
Replaces missing non-categorical values with mean of respective columns and uses KNN for missing categorical values
<H2>Usage</H2>
Use below commands in python terminal:
<ul>
>>>from missing import missing<br/>
>>>t = missing.missing(input_filename,output_filename,methods)
 </ul>methods can be "replace" or "remove"<br/>
</ul>
e.g . t = missing.missing("mydata.csv","out.csv","replace")
