

import time
import requests


from boto import mws


from boto.mws.connection import MWSConnection


count = 0

#payload = {'amazonorderid':'123123123123'}

url = 'https://api.fieldbook.com/v1/56733a810c342f030073c9d9/orders'
itemUrl = 'https://api.fieldbook.com/v1/56733a810c342f030073c9d9/orderitems'

headers = {'content-type': 'application/json', 'accept': 'application/json'}


accessKey = "accessKey"
merchantID = "merchantID"
marketplaceID = "marketplaceID"
secretKey = "secretKey"


mws = MWSConnection(accessKey, secretKey)
mws.Merchant = merchantID
mws.SellerId = merchantID
mws.MarketplaceId = marketplaceID



while month < 13:
    response = mws.list_orders(CreatedAfter = '2015-12-01T00:00:00Z', MarketplaceId = [marketplaceID])
    #if month>9:
        #response = mws.list_orders(CreatedAfter = '2015-10-01T00:00:00Z', MarketplaceId = [marketplaceID])



    orders = response.ListOrdersResult.Orders.Order

    for order in orders:
        payload = {'amazonorderid' : getattr(order, 'LatestShipDate', "Unknown"),
        'latestshipdate': getattr(order, 'LatestShipDate', "Unknown"),
        'ordertype': getattr(order, 'OrderType', "Unknown"),
        'purchasedate': getattr(order, 'PurchaseDate', "Unknown"),
        'lastupdatedate' : getattr(order, 'LastUpdateDate', "Unknown"),
        'numberofitemsshipped': getattr(order, 'NumberOfItemsShipped', "Unknown"),
        'orderstatus': getattr(order, 'OrderStatus', "Unknown"),
        'isbusinessorder': getattr(order, 'IsBusinessOrder', "Unknown"),
        'numberofitemsunshipped': getattr(order, 'NumberOfItemsUnshipped', "Unknown"),
        'buyername': getattr(order, 'BuyerName', "No Name"),
        'amount': getattr(order.OrderTotal, 'Amount', "Not Available"),
        'ispremiumorder': getattr(order, 'IsPremiumOrder', "Not Available"),
        'earliestshipdate': getattr(order, 'EarliestShipDate', "Not Available"),
        'marketplaceid': getattr(order, 'MarketplaceId', "Not Available"),
        'fulfillmentchannel': order.FulfillmentChannel,
        'paymentmethod': getattr(order, 'PaymentMethod', "Not Available"),
        'stateorregion': getattr(order.ShippingAddress, 'StateOrRegion', "No State"),
        'city': getattr(order.ShippingAddress, 'City', "No City"),
        'phone': getattr(order.ShippingAddress, 'Phone', "No Phone"),
        'countrycode': getattr(order.ShippingAddress, 'CountryCode', "No Country"),
        'postalcode': getattr(order.ShippingAddress, 'PostalCode', "No Zip"),
        'name': getattr(order.ShippingAddress, 'Name', "NO NAME"),
        'addressline1': getattr(order.ShippingAddress, 'AddressLine1', ""),
        'isprime': getattr(order, 'IsPrime', "Unknown"),
        'shipmentservicelevelcategory': getattr(order, 'ShipmentServiceLevelCategory', "Unknown") }

        request = requests.post(url, json=payload, auth=("auth", "auth"), headers=headers)
        #print (request.status_code)
        #print ((request.json()))
    #print ("Amazon Order ID: "+order.AmazonOrderId)

        itemresponse = mws.list_order_items(AmazonOrderId = order.AmazonOrderId, MarketplaceId = [marketplaceID])
        items = itemresponse.ListOrderItemsResult.OrderItems.OrderItem




        for item in items:

            itempayload = {'amazonorderid': order.AmazonOrderId,
            'quantityordered' : getattr(item, 'QuantityOrdered', "Unknown"),
            'title' : getattr(item, 'Title', "Unknown"),
            'promotiondiscountamount' : getattr(item.PromotionDiscount, 'Amount', "Unknown"),
            'asin' : getattr(item, 'ASIN', "Unknown"),
            'sellersku' : getattr(item, 'SellerSKU', "Unknown"),
            'orderitemid' : getattr(item, 'OrderItemId', "Unknown"),
            'quantityshipped' : item.QuantityShipped,
            #getattr(item, 'QuantityShipped', "Unknown"),
            'itempriceamount' : getattr(item.ItemPrice, 'Amount', "Unknown"),
            'itemtaxamount' : getattr(item.ItemTax, 'Amount', "Unknown Taxes") }

            itemrequest = requests.post(itemUrl, json=itempayload, auth=("auth", "auth"), headers=headers)
            #print ((itemrequest.json()))



            print ("Name: "+getattr(order, 'BuyerName', "No Name"))
            print ("Street Address: "+getattr(order.ShippingAddress, 'AddressLine1', ""))
            print ("State: "+getattr(order.ShippingAddress, 'StateOrRegion', "No State"))
            print ("Quantity Shipped: "+getattr(order, 'QuantityShipped', "Unknown"))
            print ("Product Name: "+getattr(item, 'Title', "Unknown"))
            print ("Phone Number: "+getattr(order.ShippingAddress, 'Phone', "No Phone"))
            print ("Order Date: "+getattr(order, 'PurchaseDate', "Unknown"))
            print ("")
            time.sleep(.9)
            month=month+1


        #print ("Order total: "+(int(item.QuantityOrdered))*((item.ItemPrice.Amount)))
