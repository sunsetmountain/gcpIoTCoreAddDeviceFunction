import base64
import logging
import json
import datetime
from google.auth import compute_engine
from apiclient import discovery
from google.cloud import iot_v1

def handle_notification(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    logging.info('New device registration info: {}'.format(pubsub_message))
    certData = json.loads(pubsub_message)['certs']
    deviceID = certData['device-id']
    publicKey = certData['publicKey']
    projectID = certData['project-id']
    cloudRegion = certData['cloud-region']
    registryID = certData['registry-id']
    newDevice = create_device(projectID, cloudRegion, registryID, deviceID, publicKey)
    logging.info('New device: {}'.format(newDevice))

def create_device(project_id, cloud_region, registry_id, device_id, public_key):
     # from https://cloud.google.com/iot/docs/how-tos/devices#api_1
     client = iot_v1.DeviceManagerClient()
     parent = client.registry_path(project_id, cloud_region, registry_id)

     # Note: You can have multiple credentials associated with a device.
     device_template = {
     #'id': device_id,
     'id' : 'testing_device',
     'credentials': [{
          'public_key': {
               'format': 'ES256_PEM',
               'key': public_key
          }
     }]
     }
     return client.create_device(parent, device_template)
