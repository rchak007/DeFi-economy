

### Chakravarti Raghavan - DeFi Total Value Locked and Automated Market makers

#### This README is for only my portion of project.

i analysed DeFi which is subset broader crypto blockchain technology use. And within Defi i specifically looked at Total Value Locked analysis and Automated Market maker trade history analysis

My Jupyter notebook and my stuff is in folder - **chuck**

##### Jupyter Notebook - [**Defi_tvl_amm.ipynb**](https://pepperdine.bootcampcontent.com/davlexic/defi-economy/-/blob/master/Chuck/Defi_tvl_amm.ipynb)

##### Excel file - exchange_trades_3.csv

##### Plot Images - in folder chuck



<u>**Motivation & Summary Slide**</u>

- Define the core message or hypothesis of your project. 

  - #### Leveraging the Crypto-currency market to create diversification in the traditional balance sheet & THE Standard portfolio.

- Describe the questions you asked, and *why* you asked them 

  - **What is DeFi -** 

  - **What are the Use cases of DeFi. -**

  - **Is DeFi growing ? and how to measure it**

  - **what are the advantages of DeFi. and does it's project future disruption**

    

- Describe whether you were able to answer these questions to your satisfaction, and briefly summarize your findings. 

  - **TVL - Total Value locked** 

    - **Total value locked has shown increased growth of $300 million, to $667 Million to $1 Billion to now $67.83 Billion in successive years since 2018. This is reflected in the data i got from DeFiPulse API.** 

  - **Automated Market maker-  an analysis was done on the TOP 10 pool token pairs on the number of trades historially. I expceted teh trades to raise as the DeFi activity rose but to my surprise i found that the number of trades did not follow the same curve as Crypto prices or Total value locked. This could be because i chose only Top 10 out of ~11500 token pairs. So if i have more time i would analyze all the 11500 token pairs than just the 10. the reason to do with Top 10 was also the API is very intense to call for each token.** 

    



**<u>Questions & Data</u>**

- Elaborate on the questions you asked, describing what kinds of data you needed to answer them and where you found it.
  - **Automated Marker Maker  - DeFiPulse API - The AMM is like a robot to set prices between 2 assets for trades. So i wanted to analyse the historical total trades activity. and see how we could use that to infer about the DeFi space.**
  - **TVL - Total Value Locked - as a measure to value DeFi.** 
  - **Used the DefiPulse API to get these data.**





**<u>Data Cleanup & Exploration</u>**

- Describe the exploration and cleanup process.

- Discuss insights you had while exploring the data that you didn't anticipate.

  - **when dealing with new APIs there could issues down the road. So its good idea to save them as a dataframe and into File to work with incase of issues.** 

- Discuss any problems that arose after exploring the data, and how you resolved them.

  - **Issue with API calls getting error 500 for Total Value locked in since couple  days. Other APIs are working. i had fortunately saved the HVPlots. But i also saved the dateframe as a File. so i could import that and work with it in future. i also posted this in their Discord App and they are looking into it now.**

  ![image-20210608145614790](/Users/chakravartiraghavan/Library/Application Support/typora-user-images/image-20210608145614790.png)

  

  * **Due to this above error my Jupyter book now has some errors in that particular part of code.** 

  - **Issue of running out of credits on the API no DefiPulse for calling the API numerous times. I opened a new email and got new API.** 
  - **Issue of realizing the History for Dexes was not through parameter and only return 30 periods and had to abondon that after i coded quite a bit to parse the data and create dataframes.**
  - **Trades API for AMM had 1000s of records for each day and also would allow to call API 1 exchange pair at a time and we had 11497 token pair assets. Also due to limits i could only get upto 3 days data at a time. So i created a date range list and for YTD data called the API 173 each for each Token pair. That would technically result in 173 * 11497 = 1,988,981 calls to the API!!!!  So i went ahead and only chose the top 10 of the Liquidity pool. That possibly skewed the data - not sure. I still expected trades would increase in the period where Total Value Locked increased. So i had more time i would redo this.** 

- Present and discuss interesting figures developed during exploration, ideally with the help of Jupyter Notebook.



Data Analysis

- Discuss the steps you took to analyze the data and answer each question you asked in your proposal.
- Present and discuss interesting figures developed during analysis, ideally with the help of Jupyter Notebook.



Discussion

- Discuss your findings. Did you find what you expected to find? If not, why not? What inferences or general conclusions can you draw from your analysis?
  - **Total value Locked although not fully accurate is a very good measure to indicate DeFi apps activity. The more the TVl usually means its being used in Lending/Borrowing/Staking in pools etc which are the Defi Apps. And was also reflective of the rise in prices for the Cryptocurrencies especially the alt coins which are big in the Defi ecosystem. So the returns in Crypto investments has to match actually DeFi applications rise too and not just some pumped up prices like Doge, Shibu meme coins. So this data will distinguish what to invest in by using at least some metrics behind it as Fundamental Analysis they use in regular Stocks.**

Postmortem

- Discuss any difficulties that arose, and how you dealt with them.
- Discuss any additional questions that came up, but which you didn't have time to answer: What would you research next, if you had two more weeks?

Questions

- Open-floor Q&A with the audience

