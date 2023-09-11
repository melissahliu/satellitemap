import ee

def initialize_gee():
    service_account = 'satmap@ee-samer.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(
        service_account, 'ee-samer-1cb0ce0fa0a0.json')
    ee.Initialize(credentials)
