# Financial-Chatbot
This is a Chatbot that can have a simple daily conversation with you and help you search stock information like: current price, latest market cap, today's volume and historical data.<br>
Stock information is obtained from [IEX Cloud](https://iexcloud.io/) using API [iexfinance](https://addisonlynch.github.io/iexfinance/devel/)<br>
The training data is created by myself, and using `RASA NLU` to be data training and processing framework of Chatbot which also use `spacy` as a frame to process natural language<br>
## Content
[Requirement](#requirement)<br>
[File Manifest](#file-manifest)<br>
[Getting Started](#getting-started)<br>
[Demo](#demo)<br>

## Requirement
1. Python<br>
2. Anaconda<br>
3. Rasa Nlu<br>`conda install -c conda-forge spacy=2.0.11`<br>`python -m spacy download en_core_web_md`<br>
4. Iexfinance<br>`pip install iexfinance`<br>or<br>`git clone https://github.com/addisonlynch/iexfinance.git`<br>
`cd iexfinance`<br>
`pip install`<br>

## File Manifest
├── Readme.md&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;// help<br>
├── Chatbot.py&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// Source program of Chatbot<br>
├── Chatbot_wechat.py&emsp;&emsp;// Source program of Chatbot on Wechat<br>
├── Chatbot_train.json&emsp;&emsp;&ensp;// Training data<br>
├── config_spacy.yml&emsp;&emsp;&emsp;// Config for spacy<br>
├── historical_data.png&emsp;&emsp;// picture formed by historical data<br>
├── WeChat_test.mp4&emsp;&emsp;// Demo of Chatbot on Wechat<br>
├── wxpy.plk &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// The buffer generated once you log in<br>

## Getting Started
Download whole project and use python to run the source programe<br>
`python Chatbot.py`<br>
Then you can communicate with Chatbot and ask him about stock information<br>
And if you want to run it on the Wechat, you need to run other programe<br>
`python Chatbot_wechat.py`<br>
Then, scan two-dimensional code ejected in your computer with your wechat.<br>
Finishing above steps, your account will be controled by Chatbot. He can help you to reply message about stock other people send to you. You can ask your friend make a test.<br>

## Demo
Here is the [Demo Video](https://github.com/dmmlcloud/Financial-Chatbot/blob/master/ChatBot/WeChat_test.mp4) of the Chatbot running on WeChat<br>
Or you can see the gif below<br>
![](https://github.com/dmmlcloud/Financial-Chatbot/blob/master/ChatBot/demo.gif)
