"""Module for IQ option websocket."""

import json
import logging
import websocket


class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def on_message(self, wss, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))

        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]

        elif message["name"] == "profile":
            self.api.profile.balance = message["msg"]["balance"]

        elif message["name"] == "candles":
            self.api.candles.candles_data = message["msg"]["candles"]
        #Make sure ""self.api.buySuccessful"" more stable
        #check buySuccessful have two fail action
        #if "user not authorized" we get buyV2_result !!!need to reconnect!!!
        #elif "we have user authoget_balancerized" we get buyComplete
        #I Suggest if you get selget_balancef.api.buy_successful==False you need to reconnect iqoption server
        elif message["name"] == "buyComplete":
            self.api.buy_successful = message["msg"]["isSuccessful"]
        elif message["name"] == "buyV2_result":
            self.api.buy_successful = message["msg"]["isSuccessful"]
        #**********************************************************   
        elif message["name"] == "listInfoData":
            listinfodata = lambda: None
            listinfodata.__dict__ = message["msg"][0]
            self.api.listinfodata.add_listinfodata(listinfodata)
        elif message["name"] == "api_option_init_all_result":
            self.api.api_option_init_all_result = message["msg"]
    @staticmethod
    def on_error(wss, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)

    @staticmethod
    def on_open(wss): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")

    @staticmethod
    def on_close(wss): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")