from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bootstrap_servers: str
    group_id: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    def get_consumer_settings(self) -> dict:
        """
        Dumps AIOKafkaConsumer specific settings

        Returns:
            a dict of AIOKafkaConsumer settings
        """
        return self.model_dump(exclude_unset=True)

    def get_producer_settings(self) -> dict:
        """
        Dumps AIOKafkaProducer specific settings

        Returns:
            a dict of AIOKafkaProducer settings
        """
        return self.model_dump(
            exclude_unset=True,
            exclude={
                "group_id",
            }
        )