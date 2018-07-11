import logging
from envparse import env
from producers.KafkaProducer import KafkaProducer
from datetime import datetime

class RobotListener:
	ROBOT_LISTENER_API_VERSION = 3
	TEST_CASE_TOPIC = "test_case_run"
	TEST_SUITE_TOPIC = "test_suite_run"
	TEST_CASE_SCHEMA = "test_case_run.avsc"
	TEST_SUITE_SCHEMA = "test_suite_run.avsc"

	def __init__(self, PARAM_ENV_VAR, OUTPUT_DIR):
		self.params = env.json(PARAM_ENV_VAR)
		self.output_dir = str(OUTPUT_DIR)
		
		# Init producer
		self.producer = KafkaProducer()
		self.producer.start()
		self.list_schemas = self.producer.load_schemas(self.TEST_CASE_SCHEMA, self.TEST_SUITE_SCHEMA)

	def create_record(self, **kwargs):
		""" Create a record """
		record = dict()
		if kwargs is not None:
			for key, value in kwargs.iteritems():
				if key == "id" and value is not None:
					record["id"] = int(value)
				elif key == "start_time":
					if value is not None:
						record["start_time"] = datetime.strptime(value, "%Y%m%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
					else:
						record["start_time"] = None
				elif key == "end_time":
					if value is not None:
						record["end_time"] = datetime.strptime(value, "%Y%m%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
					else:
						record["end_time"] = None
				elif key == "total_time":
					record["total_time"] = int(value/1000)
				elif key == "message":
					if value is not None:
						record["message"] = str(value)
					else:
						record["message"] = None
				elif key == "test_result":
					record["test_result"] = int(value)
				elif key == "test_result_dir":
					if value is not None:
						record["test_result_dir"] = str(value)
					else:
						record["test_result_dir"] = None
				elif key == "execution_status":
					record["execution_status"] = int(value)

			return record

	def start_suite(self, data, result):
		# Send record to Kafka
		record = self.create_record(id=self.params["test_suite_run_id"],
									start_time=result.starttime,
									end_time=result.endtime,
									total_time=result.elapsedtime,
									message=result.message,
									test_result_dir=None,
									execution_status=1)

		with open("listener_out.log", "ab") as log_file:
			log_file.write("--- " + str(record) + "\n")

		self.producer.produce(topic=self.TEST_SUITE_TOPIC, schema=self.list_schemas[self.TEST_SUITE_SCHEMA], record=record)
			

	def end_suite(self, data, result):
		# Send record to Kafka
		record = self.create_record(id=self.params["test_suite_run_id"],
									start_time=result.starttime,
									end_time=result.endtime,
									total_time=result.elapsedtime,
									message=result.message,
									test_result_dir=self.output_dir,
									execution_status=2)

		with open("listener_out.log", "ab") as log_file:
			log_file.write("--- " + str(record) + "\n")

		self.producer.produce(topic=self.TEST_SUITE_TOPIC, schema=self.list_schemas[self.TEST_SUITE_SCHEMA], record=record)


	def start_test(self, data, result):
		test_case_name = data.name
		list_test_case = self.params["test_case"]
		for test_case in list_test_case:
			if ("test_case_name" in test_case and str(test_case_name) == str(test_case["test_case_name"])):
				# Send record to Kafka
				record = self.create_record(id=test_case["test_case_run_id"],
											start_time=result.starttime,
											end_time=result.endtime,
											total_time=result.elapsedtime,
											message=result.message,
											test_result=0,
											execution_status=1)

				with open("listener_out.log", "ab") as log_file:
					log_file.write("---TC " + str(record) + "\n")

				self.producer.produce(topic=self.TEST_CASE_TOPIC, schema=self.list_schemas[self.TEST_CASE_SCHEMA], record=record)
	
			else:
				pass

	def end_test(self, data, result):
		test_case_name = data.name
		list_test_case = self.params["test_case"]
		for test_case in list_test_case:
			if ("test_case_name" in test_case and str(test_case_name) == str(test_case["test_case_name"])):
				test_result = 0
				if result.passed == True:
					test_result = 1
				else: 
					test_result = 2
				# Send record to Kafka
				record = self.create_record(id=test_case["test_case_run_id"],
											start_time=result.starttime,
											end_time=result.endtime,
											total_time=result.elapsedtime,
											message=result.message,
											test_result=test_result,
											execution_status=2)

				with open("listener_out.log", "ab") as log_file:
					log_file.write("---TC " + str(record) + "\n")

				self.producer.produce(topic=self.TEST_CASE_TOPIC, schema=self.list_schemas[self.TEST_CASE_SCHEMA], record=record)
	
			else:
				pass

	def output_file(self, path):
		with open("listener_out.log", "ab") as log_file:
			log_file.write("---Output " + str(path) + "\n")