# jim-cramer-estimator

An end-to-end tool for assessing the accuracy of stock commentators based on historical data.


![cramer_image](https://njmonthly.com/wp-content/uploads/cache/2015/03/CNBC_Mad_Money_Host_Jim_Cramer_2/3886020728.jpg)
## Project Description

There is an abundance of news and commentary online about the stock market. While much of the content is retrospective (determining reasons why a certain stock increased or decreased in price), some is predictive (guesses whether a stock will go up or down). Our project intends to take large numbers of past articles from common stock news sites and commentators, perform Natural Language Processing (NLP) sentiment analysis to determine the attitude of each article, and then compare that sentiment against historical stock data in order to assess the credibility of the commentator. This project will include the following sections:

- **Web Crawler**: In order to produce an abundance of stock commentary, a web crawler will be constructed to grab articles and parse them using Python and Beautiful Soup. To begin, 12 large sites will be targeted and the crawler will be constructed to process and generalize data from all of the sites.
- **Sentiment Engine**: To turn the stock articles into quantitative values for sentiment, we will either use an existing AI for the NLP analysis, or build and train our own engine using PyTorch.
- **Credibility Engine**: This engine will take sentiment about stocks and compare them with historical stock data from the TD Ameritrade API in order to determine the accuracy of each article. These scores will be aggregated and stored in a database.
- **Web Server**: A simple Flask web server will be created to serve an API with our results
- **Frontend**: A UI will be constructed to display results on a webpage, either using vanilla JS or React.

## Team Information

The members of the team are:

- Nick Zullo
    - Computer Science
    - njz12@pitt.edu
    - Graduating December 2021

- Frank Czura
    - Mechanical Engineering
    - fjc28@pitt.edu
    - Graduating August 2022

- Shane Riley
    - Mechanical Engineering, Computer Science
    - shane.riley@pitt.edu
    - Shane#7357
    - Graduating December 2022

## Project Information
### Building src environment
 - Create a virtual environment with python -m venv venv
 - Run source venv/Scripts/activate in terminal to switch to the venv
   - Exact command and file path varies by OS
 - Run python -m pip install -r requirements.txt
