from barterdude.hooks import BaseHook
from asyncworker.rabbitmq.message import RabbitMQMessage
import logging


class Logging(BaseHook):
    def __init__(
            self,
            logger: logging.Logger = logging.getLogger("barterdude")):
        self.__logger = logger

    async def before_consume(self, message: RabbitMQMessage):
        self.__logger.info(f"going to consume message: {message}")

    async def on_success(self, message: RabbitMQMessage):
        self.__logger.info(f"successfully consumed message: {message}")

    async def on_fail(self, message: RabbitMQMessage, error: Exception):
        self.__logger.error(
            f"failed to consume message ({repr(error)}): {message}"
        )
