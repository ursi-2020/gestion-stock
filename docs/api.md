[Retour à l'index](index.md)

# JSON API

## Get the stock state
Place an order in gestion-commerciale for the stocks

**Service name**: `gestion-stock`

**URL** : `api/get-all`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : order : *JsonDocument containing order's parameters*

**Content examples:** Not done yet.

## Add items to the stock
Add items (by reference and quantity) to the stock

**Service name**: `gestion-stock`

**URL** : `api/add-to-stock`

**Method** : `POST`

**Auth required** : NO

**Query Parameters** : order : *JsonDocument containing order's parameters*

**Content examples:** Not done yet.

## Add items to the stock
Remove items (by reference and quantity) from the stock and return everything removed ; if there is not enough items in the stock, nothing is done at all and a quantity of 0 is returned

**Service name**: `gestion-stock`

**URL** : `api/get-from-stock`

**Method** : `POST`

**Auth required** : NO

**Query Parameters** : order : *JsonDocument containing order's parameters*

**Content examples:** Not done yet.
