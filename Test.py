from ducktape.utils.util import wait_until
from ducktape.tests.test import Test
from ducktape.mark import matrix

from kafkatest.services.zookeeper import ZookeeperService
from kafkatest.services.kafka import KafkaService
from kafkatest.services.console_consumer import ConsoleConsumer
from kafkatest.services.kafka_log4j_appender import KafkaLog4jAppender
from kafkatest.services.security.security_config import SecurityConfig

TOPIC = "topic-log4j-appender"
MAX_MESSAGES = 100

class Log4jAppenderTest(Test):
    """
    Tests KafkaLog4jAppender using VerifiableKafkaLog4jAppender that appends increasing ints to a Kafka topic
    """
    def __init__(self, test_context):
        super(Log4jAppenderTest, self).__init__(test_context)
        self.num_zk = 1
        self.num_brokers = 1
        self.messages_received_count = 0
        self.topics = {
            TOPIC: {'partitions': 1, 'replication-factor': 1}
        }

        self.zk = ZookeeperService(test_context, self.num_zk)

    def setUp(self):
        self.zk.start()

    def start_kafka(self, security_protocol, interbroker_security_protocol):
        self.kafka = KafkaService(
            self.test_context, self.num_brokers,
            self.zk, security_protocol=security_protocol,
            interbroker_security_protocol=interbroker_security_protocol, topics=self.topics)
        self.kafka.start()

    def start_appender(self, security_protocol):
        self.appender = KafkaLog4jAppender(self.test_context, self.num_brokers, self.kafka, TOPIC, MAX_MESSAGES,
                                           security_protocol=security_protocol)
        self.appender.start()

    def custom_message_validator(self, msg):
        if msg and "INFO : org.apache.kafka.tools.VerifiableLog4jAppender" in msg:
            self.logger.debug("Received message: %s" % msg)
            self.messages_received_count += 1


    def start_consumer(self, security_protocol):
        enable_new_consumer = security_protocol != SecurityConfig.PLAINTEXT
        self.consumer = ConsoleConsumer(self.test_context, num_nodes=self.num_brokers, kafka=self.kafka, topic=TOPIC,
                                        consumer_timeout_ms=1000, new_consumer=enable_new_consumer,
                                        message_validator=self.custom_message_validator)
        self.consumer.start()

    @matrix(security_protocol=['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL'])
    def test_log4j_appender(self, security_protocol='PLAINTEXT'):
        """
        Tests if KafkaLog4jAppender is producing to Kafka topic
        :return: None
        """
        self.start_kafka(security_protocol, security_protocol)
        self.start_appender(security_protocol)
        self.appender.wait()

        self.start_consumer(security_protocol)
        node = self.consumer.nodes[0]

        wait_until(lambda: self.consumer.alive(node),
            timeout_sec=10, backoff_sec=.2, err_msg="Consumer was too slow to start")

        # Verify consumed messages count
        wait_until(lambda: self.messages_received_count == MAX_MESSAGES, timeout_sec=10,
                   err_msg="Timed out waiting to consume expected number of messages.")

        self.consumer.stop()
