import paho.mqtt.client as mqtt
import pyocr as ocr
import pyocr.builders
from PIL import Image, ImageDraw

###### Edit variables to your environment #######
broker_address = "broker.emqx.io"     #MQTT broker_address
Topic = "piper-mqtt-sy"
# Msg = "Greetings from mac pc !!!"

def pub_mqtt(__self__, Msg):
    # publish MQTT
    print("creating new instance")
    client = mqtt.Client() #create new instance

    print("connecting to broker: %s" % broker_address)
    client.connect(broker_address) #connect to broker

    print("Publishing message: %s to topic: %s" % (Msg, Topic))
    client.publish(Topic,Msg)


def main():
	img_path = "/home/pi/piper/threshold_image.jpg"
	img = Image.open(img_path)

	tools = pyocr.get_available_tools()
	if len(tools) == 0:
		print("No OCR tool found")
		sys.exit(1)
    
	tool = tools[0]
	res = tool.image_to_string(img, lang="jpn",
							builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	pub_mqtt(res)
    #if(img.mode != "RGB"):
	#	img = img.convert("RGB")
	#draw = ImageDraw.Draw(img)
	#for box in res:
	#	print(box)
	#	draw.rectangle(box.position, outline=(255, 0, 0))
	img.save("/home/pi/piper/output.jpg")
    

if __name__ == '__main__':
	main()
