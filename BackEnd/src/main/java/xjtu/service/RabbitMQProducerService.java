package xjtu.service;

public interface RabbitMQProducerService {
    String sendJsonMessage(Object jsonData);
}
