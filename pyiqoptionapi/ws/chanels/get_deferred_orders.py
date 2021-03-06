# -*- coding: utf-8 -*-
from pyiqoptionapi.ws.chanels.base import Base


class GetDeferredOrders(Base):
    
    name = "sendMessage"

    def __call__(self, instrument_type):
     
        data = {"name": "get-deferred-orders",
                "version": "1.0",
                "body": {
                          "user_balance_id": int(self.api.global_value.balance_id),
                          "instrument_type": instrument_type
                     
                        }
                }

        self.send_websocket_request(self.name, data)
