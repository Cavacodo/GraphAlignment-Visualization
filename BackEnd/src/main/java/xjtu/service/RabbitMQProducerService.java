package xjtu.service;

public interface RabbitMQProducerService {
    void sendJsonMessage(Object jsonData);
}
