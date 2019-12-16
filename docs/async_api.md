[Retour à l'index](index.md)

# Asynchronous API

## Input messages

### Business Intelligence : get_stock

**from**: `business-intelligence`

**functionname** : `get_stock`

**body** : empty

### Gestion Commerciale : resupply

**from**: `gestion-commerciale`

**functionname** : `resupply`

**body** :
```json
{
  "idCommande": 1000,
  "produits":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```

### Gestion Commerciale : delivery

**from**: `gestion-commerciale`

**functionname** : `delivery`

**body** : 
```json
{
  "idCommande": 1000,
  "produits":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```

## Output messages

### Gestion Commerciale : get_stock_order_response

**to**: `gestion-commerciale`

**functionname** : `get_stock_order_response`

**body** : 
```json
{
  "idCommande": 1000,
  "produits":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```

### Gestion Commerciale : get_stock

**to**: `gestion-commerciale`

**functionname** : `get_stock`

**body** : 
```json
[
  {"codeProduit": "XXX", "quantite": 10}
]
```

### Business Intelligence : get_stock

**to**: `business_intelligence`

**functionname** : `get_stock`

**body** : 
```json
{
  "stock":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```

### Business Intelligence : get_resupply

**to**: `business-intelligence`

**functionname** : `get_resupply`

**body** : 
```json
{
  "idCommande": 1000,
  "produits":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```

### Business Intelligence : get_delivery

**to**: `business-intelligence`

**functionname** : `get_delivery`

**body** : 
```json
{
  "idCommande": 1000,
  "produits":
  [
    {"codeProduit": "XXX", "quantite": 10}
  ]
}
```
