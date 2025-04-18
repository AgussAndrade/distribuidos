#!/usr/bin/env python3
import pika
import signal
import sys
import time
import logging
import json
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Producer:
    def __init__(self, queue_name: str = 'default'):
        self._queue_name = queue_name
        self._connection = None
        self._channel = None
        self._closing = False
        signal.signal(signal.SIGTERM, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        logger.info('SIGTERM recibido - Iniciando graceful shutdown')
        self._closing = True
        if self._connection:
            self._notify_shutdown()
            self._connection.close()

    def connect(self) -> bool:
        """Establece conexión con RabbitMQ y configura el exchange"""
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self._channel = self._connection.channel()

            # Declarar exchange direct
            self._channel.exchange_declare(
                exchange='direct_exchange',
                exchange_type='direct',
                durable=True
            )

            # Declarar la cola para asegurar que existe
            self._channel.queue_declare(
                queue=self._queue_name,
                durable=True
            )

            # Vincular la cola al exchange
            self._channel.queue_bind(
                exchange='direct_exchange',
                queue=self._queue_name,
                routing_key=self._queue_name
            )

            logger.info(f"✅ Productor conectado a la cola: {self._queue_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Error al configurar productor: {e}")
            return False

    def enqueue(self, message: Any) -> bool:
        """Encola un mensaje en RabbitMQ"""
        try:
            if not self._connection or self._connection.is_closed:
                if not self.connect():
                    return False

            # Publicar mensaje al exchange direct
            self._channel.basic_publish(
                exchange='direct_exchange',
                routing_key=self._queue_name,
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # hace el mensaje persistente
                )
            )

            logger.info(f"📤 Mensaje enviado: {message}")
            return True

        except Exception as e:
            logger.error(f"❌ Error al enviar mensaje: {e}")
            return False

    def _notify_shutdown(self):
        """Notifica a los consumidores que el productor se está cerrando"""
        shutdown_message = {
            "type": "shutdown",
            "timestamp": time.time(),
            "message": "Producer se está cerrando"
        }
        self.enqueue(shutdown_message)
        logger.info("Notificación de shutdown enviada a los consumers")

    def close(self):
        """Cierra la conexión con RabbitMQ"""
        try:
            if self._connection and not self._connection.is_closed:
                self._notify_shutdown()
                self._connection.close()
                logger.info("✅ Conexión cerrada correctamente")
        except Exception as e:
            logger.error(f"❌ Error al cerrar conexión: {e}")