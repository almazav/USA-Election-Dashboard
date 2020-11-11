# USA-Election-Dashboard

In this project a jupyter notebook(automatic data colectionipynb). was created with the steps to follow to extract USA election data from https://eu.usatoday.com/elections/results/race/2020-11-03-presidential/.
Using the extarcted data a dataframe was created in order to analyse it in a better way.
Plots of the relevant data were created, and Dataframe in the final form was uploded to an AWS s3 bucket for further extraction.

Following this steps an automated data updating system was created using AWS EC2 in order to update the file in the previously created s3 bucket.(in oreder to achive this the jupyter notebook file was not used as the configuration its more complicated then a automated_data.py file was created)

Finally a Dashboard (usa_map.py)with the data created by The EC2 instance was created and uploaded in heroku https://usa-election-graphs.herokuapp.com/
