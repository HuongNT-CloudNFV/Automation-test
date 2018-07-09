from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import json
import logging
import os
from datetime import datetime

class KafkaProducer(object):
	def __init__(self):
		# Path to config file
		self.config_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'config')
		self.config_file = os.path.join(self.config_dir, "producer.json")

		# Path to schema file
		self.avsc_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'schemas')

		# Setup logger
		logging.basicConfig(level=logging.INFO,
							format='%(asctime)s - %(levelname)s - %(message)s')
		self.logger = logging.getLogger(__name__)	

	def init_config(self):
		with open(self.config_file, "r") as config_file:
			config = json.loads(config_file.read())
			for key in config:
				config[key] = config[key].encode("ascii")
			self.config = {
				"bootstrap.servers": config["bootstrap.servers"],
				"schema.registry.url": config["schema.registry.url"]
			}
		self.logger.info("Import configuration file")
		self.logger.info("Bootstrap Servers: {}".format(self.config["bootstrap.servers"]))
		self.logger.info("Schema Registry: {}".format(self.config["schema.registry.url"]))

	def create_producer(self):
		self.producer = AvroProducer(self.config)
		self.logger.info("Start Producer")

	def load_schemas(self, *argv):
		""" Return a dict mapping schema name with loaded schema object """
		list_schema = dict()
		for schema in argv:
			created_schema = avro.load(os.path.join(self.avsc_dir, str(schema)))
			self.logger.info("Loading schema {}".format(schema))
			list_schema[str(schema)] = created_schema

		return list_schema

	def produce(self, topic, schema, record):
		""" Produce new record """
		try:
			self.producer.produce(topic=topic,
							value_schema=schema,
							value=record)
			self.producer.flush()
			self.logger.info("Produce new record {}".format(record))
		except Exception as e:
			self.logger.error(e)

	def start(self):
		self.init_config()
		self.create_producer()

