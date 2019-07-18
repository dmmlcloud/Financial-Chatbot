# Financial-Chatbot
This is a Chatbot that can have a simple daily conversation with you and help you search stock information like: current price, latest market cap, today's volume and historical data.<br>
Stock information is obtained from [IEX Cloud](https://iexcloud.io/) using API [iexfinance](https://addisonlynch.github.io/iexfinance/devel/)<br>
The training data is created by myself, and using `RASA NLU` to be data training and processing framework of Chatbot which also use `spacy` as a frame to process natural language<br>
## Content
[Requirement](#requirement)<br>
[File Manifest](#-file-manifest)<br>
[Getting Started](#-getting-started)<br>
[Demo](#-demo)<br>

## Requirement
1. Python<br>
2. Anaconda<br>
3. Rasa Nlu<br>`conda install -c conda-forge spacy=2.0.11`<br>`python -m spacy download en_core_web_md`<br>
4. Iexfinance<br>`pip install iexfinance`<br>or<br>`git clone https://github.com/addisonlynch/iexfinance.git`<br>
`cd iexfinance`<br>
`pip install`<br>

## File Manifest
├── Readme.md&emsp;&emsp;// help<br>
├── Chatbot.py                    // Source program of Chatbot<br>
├── Chatbot_wechat.py             // Source program of Chatbot on Wechat<br>
├── Chatbot_train.json            // Training data<br>
├── config_spacy.yml              // Config for spacy<br>
├── historical_data.png           // picture formed by historical data<br>
├── WeChat_test.mp4               // Demo of Chatbot on Wechat<br>
├── wxpy.plk                      // The buffer generated once you log in<br>

## Getting Started

## Demo

