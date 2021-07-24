import csv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()

##file_path = "Book1.csv"
collection_name = "news"

def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def get_data_item(item, data_type):
	# Add other data types you want to handle here
    if data_type == 'int':
        return int(item)
    elif data_type == 'bool':
        return bool(item)
    else:
        return item





