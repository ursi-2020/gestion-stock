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
