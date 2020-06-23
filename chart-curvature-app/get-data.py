from __future__ import print_function
from datetime import datetime
from time import time
import logging
from operator import itemgetter
from pymongo import MongoClient
import pandas as pd
import numpy as np
import sys

# Extra plotly bits
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# Init logger
logger = logging.getLogger(__name__)

class Chart(object):
    """ Saves and retrieves chart data to/from mongodb. It saves the chart
    based on candle size, and when called, it will automaticly update chart
    data if needed using the timestamp of the newest candle to determine how
    much data needs to be updated """

    def __init__(self, api, pair, **kwargs):
        """
        api = poloniex api object
        pair = market pair
        period = time period of candles (default: 2 HOURS)
        start = start time in UNIX timestamp format
        end = end time in UNIX timestamp format
        """
        self.pair = pair
        self.api = api
        self.period = kwargs.get('period', self.api.HOUR * 2)
        # START: Default is to go back 1 year.
        self.start = kwargs.get('start', (time() - self.api.YEAR))
        # END: Default is the current moment. With no value provided here
        # we fallback to current time.
        self.end = kwargs.get('end', False)
        self.db = MongoClient()['poloniex']['%s_%s_chart' %
                                            (self.pair, str(self.period))]

    def __call__(self, size=0):
        """ Returns raw data from the db, updates the db if needed """
        # get old data from db
        old = sorted(list(self.db.find()), key=itemgetter('_id'))
        try:
            # get last candle
            last = old[-1]
        except:
            # no candle found, db collection is empty
            last = False
        # no entrys found, get last year of data to fill the db
        if not last:
            logger.warning('%s collection is empty!',
                           '%s_%s_chart' % (self.pair, str(self.period)))
            logger.info('Data request for {PERIOD: %s, START: %s, END: %s}' % (str(self.period), str(self.start), str(self.end)))
            new = self.api.returnChartData(self.pair,
                                           period=self.period,
                                           start=self.start,
                                           end=self.end)
        # we have data in db already
        else:
            logger.warning('Updating existing collection for %s',
                           '%s_%s_chart' % (self.pair, str(self.period)))
            logger.info('Data request for {PERIOD: %s, START: %s, END: %s}' % (str(self.period), str(self.start), str(self.end)))
            new = self.api.returnChartData(self.pair,
                                           period=self.period,
                                           start=int(last['_id']),
                                           end=self.end)
        # add new candles
        updateSize = len(new)
        logger.info('Updating %s with %s new entries!',
                    self.pair + '-' + str(self.period), str(updateSize))
        # show progress
        for i in range(updateSize):
            print("\r%s/%s" % (str(i + 1), str(updateSize)), end=" complete ")
            date = new[i]['date']
            del new[i]['date']
            self.db.update_one({'_id': date}, {"$set": new[i]}, upsert=True)
        print('')
        logger.debug('Getting chart data from db')
        # return data from db
        return sorted(list(self.db.find()), key=itemgetter('_id'))[-size:]

    def dataFrame(self, size=0, window=120):
        # get data from db
        data = self.__call__(size)
        # make dataframe
        df = pd.DataFrame(data)
        # format dates
        df['date'] = [pd.to_datetime(c['_id'], unit='s') for c in data]
        # Recast
        df['timestamp'] = df['_id']
        df['date_label'] = df['date'].map(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S"))
        del df['_id']
        # set 'date' col as index
        df.set_index('date', inplace=True)
        # Return structured data-set.
        return df

if __name__ == '__main__':
    from poloniex import Poloniex
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("poloniex").setLevel(logging.INFO)
    logging.getLogger('requests').setLevel(logging.ERROR)
    api = Poloniex(jsonNums=float)

    # Target ticker is Stratis (BTC/STRAT pair on Poloniex).
    # period = 2 hours
    df = Chart(api, 'BTC_STRAT', period=(api.HOUR * 2)).dataFrame()
    df.dropna(inplace=True)

    # Debug
    logger.debug('Incoming data [tail]:')

    # Access required data fields as a test.
    print(df.tail())

    # CSV dumping stage so we can keep plotting as a separate process.
    df.to_csv('data.csv')
