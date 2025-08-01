# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2624ur7vnlfja-ats.iot.eu-west-3.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "../certificates/8bf58fa0a2b784fddedc6144e3a92f9b14f0ddcd263cf79a016013073ff9f238-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "../certificates/8bf58fa0a2b784fddedc6144e3a92f9b14f0ddcd263cf79a016013073ff9f238-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../certificates/AmazonRootCA1.pem"
TOPIC = "test/anemometer"
MESSAGE = "Publicado no topico: " + TOPIC
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: '" + TOPIC)
    t.sleep(0.1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()