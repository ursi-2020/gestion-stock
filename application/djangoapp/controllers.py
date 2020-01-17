from django.http import *
from .utils import *
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False

# Returns the stock status
def get_stock():
    stock = Article.objects.values()
    ret = list(stock)
    return ret

# Returns the stock status for a specific product
def get_product(id):
    return

# Adds a resupply to the stock
def add_to_stock():
    return

# Removes a delivery from the stock
def remove_from_stock():
    return

# Sends an async message to gestion-commerciale to ask for resupply
def ask_for_resupply():
    allStock = {"stock": get_stock()}
    sendAsyncMsg('gestion-commerciale', allStock, "get_stock")

# Makes a modification in the stock # FIXME Fix this shit
def stock_modif_from_body(order):
    print_info("Stock modif from body", [
        ("order", order)
    ])
    livraison = 1 if order["livraison"] else -1
    list = order["produits"]
    # Dictionnary to create Entry object before rendering
    entry = {}
    entry["idCommande"] = order["idCommande"]
    command = []
    newProduct = []
    for produit in list:
        product = {}
        codeProduit = produit["codeProduit"]
        delivered = produit["quantite"]
        try:
            instance = Article.objects.get(codeProduit=codeProduit)
        except Article.DoesNotExist:
            instance = None
        # Object exist in stock
        if instance is not None:
            # GesCo ordered more than what's in stock
            if not order["livraison"] and instance.quantite < produit["quantite"]:
                delivered = 0
            instance.quantite += delivered * livraison
            instance.save()
            logger.info("Article " + str(instance.codeProduit) + " was sucessfully updated : new stock value : " + str(instance.quantite))
        # Object doesn't exist in stock
        else:
            # Requesting object not in base ==> Inserting in base with quantity 0
            if not order["livraison"]:
                delivered = 0
                #newProduct = Article.objects.create(
                 #   codeProduit=codeProduit,
                  #  quantite=produit["quantite"]
                #)
                #logger.info("Article " + str(newProduct.codeProduit) + " was sucessfully created : new stock value : " + str(newProduct.quantite))
            # Handles all other cases (insertion in base)
            newProduct.append(Article(codeProduit=codeProduit, quantite=delivered))
        product["codeProduit"] = codeProduit
        product["quantite"] = delivered
        command.append(product)
    # Bulk Creating articles, trying out solution to fix problem
    Article.objects.bulk_create(newProduct)
    # Creating Entry item for Logs
    entry["produits"] = command
    package = json.dumps(entry, indent=2)
    date = datetime.now()
    Entry.objects.create(
        package=package,
        date=date,
        delivery=True if livraison > 0 else False
    )
    logger.info("Entry created : package was : " + package + ", at : " + date.strftime("%Y-%b-%d, %H:%M:%S"))
    return entry