
import os
import time

import paho.mqtt.client as mqtt
import requests

###########################################################
#####  Set constant values for MQTT broker   ##############

BrokerAddress = "broker.emqx.io"    # Cloud MQTT
MqttTopic = "piper-mqtt-sy"
text = 'text'
TOKEN = os.environ.get('TOKEN')
###########################################################
#####  Define functions   #################################

# HasuraCloud
query = """
mutation CreateMutation($COMMENT: String, $DATE: date, $SUM: Int) {
  insert_Housekeeping_Note_one(object: {DATE: $DATE, SUM: $SUM, COMMENT: $COMMENT}) {
    ID
    DATE
    SUM
    COMMENT
  }
}
"""
url_hasura = "https://piper-project.hasura.app/v1beta1/relay"
headers_hasura = {
    'Hasura-Client-Name':'hasura-console',
    'x-hasura-admin-secret':os.environ.get('HASURA_SECRET'),
    'content-type':'application/json'
}


# LineNotify
headers = {
    'Authorization':"Bearer "+TOKEN,
}

def on_message(client, userdata, message):  ### callback when get message from MQTT broker
    msg = str(message.payload.decode("utf-8"))
    print("Message received:" + msg)


    
    variables = {
        'COMMENT':msg,
        'DATE':'2021-12-13',
        'SUM':0,
    }
    data={"query":query,"variables":variables}
    # HTTP POST to Hasura Cloud
    res = requests.post(url=url_hasura,headers=headers_hasura,json=data)
    

    files = {
        'message':(None,str(msg)),
    }
    # HTTP POST to LineNotify
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

###########################################################
#####  Main                     ###########################

def main():
    ### Connect MQTT broker 
    print("Connecting to MQTT broker:" + BrokerAddress)
    client = mqtt.Client()               # Create new instance with Any clientID
    client.on_message=on_message         # Attach function to callback
    try:
        client.connect(BrokerAddress)    #connect to broker
    except:
        print("***** Broker connection failed *****")
        exit(1) 

    ### Subscribe ###
    print("Subscribe topic:", MqttTopic)
    client.subscribe(MqttTopic)          # Subscribe MQTT

    ### loop forever to wait a message ###
    print("Waiting message...")
    client.loop_forever()                # Loop forever

if __name__ == '__main__':
    main()
