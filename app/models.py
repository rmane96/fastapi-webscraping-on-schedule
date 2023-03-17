from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid




class Product(Model):
    __keyspace__ = "webscraper"
    asin = columns.Text(primary_key=True,required=True) # amazons unique id number, using for indexing
    title = columns.Text()
    price_str = columns.Text()
    

# only detail view
class ProductScrapeEvent(Model):
    __keyspace__ = "webscraper"
    uuid = columns.UUID(primary_key=True)
    asin = columns.Text(index=True) # amazons unique id number, using for indexing
    title = columns.Text()
    price_str = columns.Text()