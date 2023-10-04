# marketdata_server
# Marketdata_server

Framework for establishing connections to real time market data servers. Consuming the data into a standard format and storing it to a file, database or both. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The things you need before installing the software.

import socket
import select
import time
import sys
import unicodedata as unicode
from store import Storage
import queue
from symbols import Symbol_map
import configparser
import threading 
from yahoo_handler import yahoo_handler
import datetime as dt
import pandas as pd 
import sqlalchemy


