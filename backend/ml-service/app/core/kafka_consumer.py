"""Kafka consumer for real-time feature updates."""
import asyncio
import json
from typing import Optional

import structlog
from aiokafka import AIOKafkaConsumer
from app.core.config import settings
from app.core.cache import cache_manager
from app.services.feature_store import feature_store

logger = structlog.get_logger()


class KafkaLifecycle:
    def __init__(self) -> None:
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        try:
            self._consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC_CUSTOMER_EVENTS,
                settings.KAFKA_TOPIC_TRANSACTION_EVENTS,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP,
                group_id=settings.KAFKA_CONSUMER_GROUP,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")) if v else None,
            )
            await self._consumer.start()
            self._task = asyncio.create_task(self._consume_loop())
            logger.info("kafka.consumer_started")
        except Exception as e:
            logger.warning("kafka.start_failed", error=str(e))

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def _consume_loop(self) -> None:
        assert self._consumer is not None
        try:
            async for msg in self._consumer:
                try:
                    event = msg.value
                    event_type = event.get("eventType", "")
                    payload = event.get("payload", {})

                    if event_type == "customer.updated":
                        await feature_store.invalidate_customer(payload.get("customerId"))
                    elif event_type == "transaction.created":
                        await feature_store.update_transaction_features(payload)
                except Exception as e:
                    logger.error("kafka.message_handler_failed", error=str(e), offset=msg.offset)
        except asyncio.CancelledError:
            pass


kafka_lifecycle = KafkaLifecycle()
