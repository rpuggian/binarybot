# Binarybot

A trader bot to automate a trade execution scheduling it at IQoption.com 

## How to schedule your trades? 

All trades are scheduleds using a CSV in the following format: 

| ACTIVE  | BUY TIME | ACTION | VALUE |
|---------|----------|--------|-------|
| EUR/USD | 09:31    | PUT    | 2     |


## Usage

After fill the csv with your trades, run the bot using: 

``` 
python bot.py
```

Type all needed information and your IQoption credentials to start.
