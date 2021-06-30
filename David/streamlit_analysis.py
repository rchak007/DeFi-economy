import streamlit as st
import pandas as pd
import numpy as np
from cryptocmd import CmcScraper
import datetime


class MCSimulation:
    """
    A Python class for running Monte Carlo simulation on portfolio price data. 
    
    ...
    
    Attributes
    ----------
    portfolio_data : pandas.DataFrame
        portfolio dataframe
    weights: list(float)
        portfolio investment breakdown
    nSim: int
        number of samples in simulation
    nTrading: int
        number of trading days to simulate
    simulated_return : pandas.DataFrame
        Simulated data from Monte Carlo
    confidence_interval : pandas.Series
        the 95% confidence intervals for simulated final cumulative returns
        
    """
    
    def __init__(self, portfolio_data, weights="", num_simulation=1000, num_trading_days=252):
        """
        Constructs all the necessary attributes for the MCSimulation object.

        Parameters
        ----------
        portfolio_data: pandas.DataFrame
            DataFrame containing stock price information from Alpaca API
        weights: list(float)
            A list fractions representing percentage of total investment per stock. DEFAULT: Equal distribution
        num_simulation: int
            Number of simulation samples. DEFAULT: 1000 simulation samples
        num_trading_days: int
            Number of trading days to simulate. DEFAULT: 252 days (1 year of business days)
        """
        
        # Check to make sure that all attributes are set
        if not isinstance(portfolio_data, pd.DataFrame):
            raise TypeError("portfolio_data must be a Pandas DataFrame")
            
        # Set weights if empty, otherwise make sure sum of weights equals one.
        if weights == "":
            num_stocks = len(portfolio_data.columns.get_level_values(0).unique())
            weights = [1.0/num_stocks for s in range(0,num_stocks)]
        else:
            if round(sum(weights),2) < .99:
                raise AttributeError("Sum of portfolio weights must equal one.")
        
        # Calculate daily return if not within dataframe
        if not "daily_return" in portfolio_data.columns.get_level_values(1).unique():
            close_df = portfolio_data.xs('Close',level=1,axis=1).pct_change()
            tickers = portfolio_data.columns.get_level_values(0).unique()
            column_names = [(x,"daily_return") for x in tickers]
            close_df.columns = pd.MultiIndex.from_tuples(column_names)
            portfolio_data = portfolio_data.merge(close_df,left_index=True,right_index=True).reindex(columns=tickers,level=0)    
        
        # Set class attributes
        self.portfolio_data = portfolio_data
        self.weights = weights
        self.nSim = num_simulation
        self.nTrading = num_trading_days
        self.simulated_return = ""
        
    def calc_cumulative_return(self):
        """
        Calculates the cumulative return of a stock over time using a Monte Carlo simulation (Brownian motion with drift).

        """
        
        # Get closing prices of each stock
        last_prices = self.portfolio_data.xs('Close',level=1,axis=1)[-1:].values.tolist()[0]
        
        # Calculate the mean and standard deviation of daily returns for each stock
        daily_returns = self.portfolio_data.xs('daily_return',level=1,axis=1)
        mean_returns = daily_returns.mean().tolist()
        std_returns = daily_returns.std().tolist()
        
        # Initialize empty Dataframe to hold simulated prices
        portfolio_cumulative_returns = pd.DataFrame()
        
        # Run the simulation of projecting stock prices 'nSim' number of times
        for n in range(self.nSim):
        
            if n % 10 == 0:
                print(f"Running Monte Carlo simulation number {n}.")
        
            # Create a list of lists to contain the simulated values for each stock
            simvals = [[p] for p in last_prices]
    
            # For each stock in our data:
            for s in range(len(last_prices)):

                # Simulate the returns for each trading day
                for i in range(self.nTrading):
        
                    # Calculate the simulated price using the last price within the list
                    simvals[s].append(simvals[s][-1] * (1 + np.random.normal(mean_returns[s], std_returns[s])))
    
            # Calculate the daily returns of simulated prices
            sim_df = pd.DataFrame(simvals).T.pct_change()
    
            # Use the `dot` function with the weights to multiply weights with each column's simulated daily returns
            sim_df = sim_df.dot(self.weights)
    
            # Calculate the normalized, cumulative return series
            portfolio_cumulative_returns[n] = (1 + sim_df.fillna(0)).cumprod()
        
        # Set attribute to use in plotting
        self.simulated_return = portfolio_cumulative_returns
        
        # Calculate 95% confidence intervals for final cumulative returns
        self.confidence_interval = portfolio_cumulative_returns.iloc[-1, :].quantile(q=[0.025, 0.975])
        
        return portfolio_cumulative_returns
    
    def plot_simulation(self):
        """
        Visualizes the simulated stock trajectories using calc_cumulative_return method.

        """ 
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return,pd.DataFrame):
            self.calc_cumulative_return()
            
        # Use Pandas plot function to plot the return data
        plot_title = f"{self.nSim} Simulations of Cumulative Portfolio Return Trajectories Over the Next {self.nTrading} Trading Days."
        return self.simulated_return.plot(legend=None,title=plot_title)
    
    def plot_distribution(self):
        """
        Visualizes the distribution of cumulative returns simulated using calc_cumulative_return method.

        """
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return,pd.DataFrame):
            self.calc_cumulative_return()
        
        # Use the `plot` function to create a probability distribution histogram of simulated ending prices
        # with markings for a 95% confidence interval
        plot_title = f"Distribution of Final Cumuluative Returns Across All {self.nSim} Simulations"
        plt = self.simulated_return.iloc[-1, :].plot(kind='hist', bins=10,density=True,title=plot_title)
        plt.axvline(self.confidence_interval.iloc[0], color='r')
        plt.axvline(self.confidence_interval.iloc[1], color='r')
        return plt
    
    def summarize_cumulative_return(self):
        """
        Calculate final summary statistics for Monte Carlo simulated stock data.
        
        """
        
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_return,pd.DataFrame):
            self.calc_cumulative_return()
            
        metrics = self.simulated_return.iloc[-1].describe()
        ci_series = self.confidence_interval
        ci_series.index = ["95% CI Lower","95% CI Upper"]
        return metrics.append(ci_series)

st.title("Cryptocurrency Analysis")
tokens=("BTC",
    "ETH", 
    "DOT",
    "ADA",
    'LINK',
    'XRP',
    'BNB',
    'DOGE',
    'UNI',
    'BCH',# 10
    'MATIC',
    'XLM',
    'SOL',
    'VET',
    'ETC',
    'EOS',
    'TRX',
    'FIL',
    'XMR',
    'AAVE'#20
    )
add_selectbox = st.sidebar.selectbox(
    "What Token you like to be analyzed?",
    ("BTC",
    "ETH", 
    "DOT",
    "ADA",
    'LINK',
    'XRP',
    'BNB',
    'DOGE',
    'UNI',
    'BCH',# 10
    'MATIC',
    'XLM',
    'SOL',
    'VET',
    'ETC',
    'EOS',
    'TRX',
    'FIL',
    'XMR',
    'AAVE'#20
    )
)
st.write('## Data Analysis')
st.write('''#### Hello, this application will return analysis for selected tokens on the left side. PLease select from the drop down on the left side and start to explore''')
if st.checkbox('Show Analysis of Token'):

    st.write(f'running for {add_selectbox}')
    scraper=CmcScraper(add_selectbox).get_dataframe()

    scraper.set_index('Date', inplace=True)

    cprod= np.cumprod(1+ scraper.iloc[::-1]['Close'].pct_change().dropna())-1
    sharpe_ratio = ((scraper.iloc[::-1]['Close'].pct_change().mean()) * 252) / (scraper.iloc[::-1]['Close'].pct_change().std() * np.sqrt(252))

    st.write(scraper.iloc[::-1].head())
    st.write('## Line Chart')
    st.line_chart(scraper['Close'])
    st.write('## Rolling window for 30 days')
    st.line_chart(scraper.iloc[::-1]['Close'].rolling(window=30).mean().dropna())
    st.write('Percent Change')
    st.area_chart(scraper.iloc[::-1]['Close'].pct_change().dropna())
    st.write('sharpe ratio')
    st.write(sharpe_ratio)
    st.write('## cumulative returns')
    st.line_chart(cprod)
    



### sharpe ratio effective frontier
st.write('## Porfolio and weight analysis')
st.write('#### To analysis a specific cryptocurrency porfolio please select atleast two tokens from the drop down on the left and then select submit. ')
with st.form("Portfolio"):
    token_selected= st.sidebar.multiselect('analysis your portfolio (must select two or more)',tokens)
    submitted = st.form_submit_button("Submit")
    if token_selected ==[]:
        st.write('## please add token to portfolio')
    else:
        separator = ", "
        st.write(f'your portfolio contains {separator.join(token_selected)}')
    if submitted:
        portfolio=[]
## creating portfolio
        
## pulling data frame 

        for x in token_selected:
            portfolio.append(CmcScraper(x).get_dataframe(date_as_index=True)['Close'])
            token_df = pd.DataFrame(portfolio)
        corrected_tbl=token_df.transpose()
        corrected_tbl.columns=token_selected
        corrected_tbl.index = corrected_tbl.index.date
        st.write('### Dataframe')
        st.write(corrected_tbl.head())
        st.write('### Historical Growth')
        st.line_chart(corrected_tbl)
        
## Present the data
        ## Formulas
        closed_pct_change=corrected_tbl.pct_change().dropna()
        mean_daily_return=corrected_tbl.pct_change().dropna().mean()
        correlation=corrected_tbl.pct_change().dropna().corr()
        stock_normed = corrected_tbl.dropna()/corrected_tbl.dropna().iloc[0]
        log_ret = np.log(corrected_tbl/corrected_tbl.shift(1))
        log_mean=log_ret.mean() * 252
        log_covarriance=log_ret.cov()
        year_log_cov=log_ret.cov()*252
        correlation=corrected_tbl.dropna().corr()
        
        ## charting
        st.write('## Token Normalized Chart')
        st.area_chart(stock_normed)
        st.write('## Logarithmic Variance')
        st.bar_chart(log_ret)
        col3, col4 = st.beta_columns(2)
        with col3:
                st.write('### Correlation')
                st.write(correlation)
        with col4:
                st.write('### annual Covariance(Log)')
                st.write(year_log_cov)
        num_ports = 1000
        all_weights = np.zeros((num_ports,len(corrected_tbl.columns)))
        ret_arr = np.zeros(num_ports)
        vol_arr = np.zeros(num_ports)
        sharpe_arr = np.zeros(num_ports)
        st.write('## Best portfolio weight assessment based on sharpe ratio')
        import time
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        for ind in range(num_ports):

    # Create Random Weights
            weights = np.array(np.random.random(len(token_selected)))
    # Rebalance Weights
            weights = weights / np.sum(weights)  
    # Save Weights
            all_weights[ind,:] = weights
    # Expected Return
            ret_arr[ind] = np.sum((log_ret.mean() * weights) *252)
    # Expected Variance
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    # Sharpe Ratio
            sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
    # Sharpe Return
            sharpe_Return=sharpe_arr.max()
    # Sharpe Max
            sharpe_max=sharpe_arr.argmax()
    # Best weights
            best_weights=all_weights[sharpe_max,:]
            max_sr_ret = ret_arr[sharpe_max]
            max_sr_vol = vol_arr[sharpe_max]
            rounded_weights=best_weights.round(2).astype("str")
        st.write('## best weights for your portfolio')
        st.write( f' {token_selected}: {rounded_weights}')
        corrected_tbl.columns=pd.MultiIndex.from_product([corrected_tbl,['Close']])
        st.write('### calculating projected returns in 5 years') 
        my_bar2 = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar2.progress(percent_complete + 1) 
        MC_portfolio = MCSimulation(
        portfolio_data = corrected_tbl,
        num_simulation = 250,
        num_trading_days = 252*5,
        weights= best_weights
        )
        MC_portfolio.calc_cumulative_return()
        simulated_returns_data = {
        "mean": list(MC_portfolio.simulated_return.mean(axis=1)),
        "median": list(MC_portfolio.simulated_return.median(axis=1)),
        "min": list(MC_portfolio.simulated_return.min(axis=1)),
        "max": list(MC_portfolio.simulated_return.max(axis=1))
        }
        df_simulated_returns = pd.DataFrame(simulated_returns_data)
        portfolio_tbl=MC_portfolio.summarize_cumulative_return()
        st.line_chart(df_simulated_returns)
        port_ci_lower = round(portfolio_tbl[8]*50000,2)
        port_ci_upper = round(portfolio_tbl[9]*50000,2)
        port_ci_min = round(portfolio_tbl[3]*50000,2)
        # Print results
        dist_plot = MC_portfolio.plot_distribution()
        st.write(f"There is a 95% chance that an initial investment of $50,000 in the portfolio"
        f" over the next 5 years will end within in the range of"
        f" ${port_ci_lower} and ${port_ci_upper}. and a minimum return of ${port_ci_min}")
        st.write(portfolio_tbl)
        st.balloons() 
        
        






            



