##########################
# RabbitMQ for webcrawling
# for Ubuntu: sudo apt-get install python-pip git-core
##########################

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
	'localhost'))
channel = connection.channel()