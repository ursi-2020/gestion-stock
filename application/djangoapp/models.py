from django.db import models


class Article(models.Model):
    idProduit = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)


class Entry(models.Model):
    # package is a JSON formatted string that will store the id and the quantity moved
    package = models.TextField
    date = models.DateTimeField()

    def __str__(self):
        return 'Entry: {} - {}'.format(self.package, self.date)


class Produit(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "{\"codeProduit\":{}, \"familleProduit\":{}, \"descriptionProduit\":{},\"quantiteMin\":{}, \"packaging\":{}, \"prix\":{}}".format(
            self.codeProduit, self.familleProduit, self.descriptionProduit, self.quantiteMin, self.packaging, self.prix)

