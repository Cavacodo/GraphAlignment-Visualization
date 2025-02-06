package xjtu.service.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.service.RabbitMQProducerService;

import java.util.UUID;

@Service
public class RabbitMQProducerServiceImpl implements RabbitMQProducerService {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Override
    public String sendJsonMessage(Object jsonData) {
        try {
            String jsonStr = new ObjectMapper().writeValueAsString(jsonData);
            String correlationId = UUID.randomUUID().toString();
            CorrelationData correlationData = new CorrelationData(correlationId);

            // 设置回调
            rabbitTemplate.setReturnsCallback((returned) -> {
                System.out.println("Failed to send message: " + new String(returned.getMessage().getBody()));
            });

            rabbitTemplate.setConfirmCallback((correlationData1, ack, cause) -> {
                if (ack) {
                    System.out.println("Message sent successfully with correlationId: " + correlationData1.getId());
                } else {
                    System.out.println("Message failed to send with correlationId: " + correlationData1.getId() + ", cause: " + cause);
                }
            });

            // 创建消息
            MessageProperties messageProperties = new MessageProperties();
            messageProperties.setCorrelationId(correlationId);
            messageProperties.setContentType("application/json"); // 设置内容类型为 JSON
            Message message = new Message(jsonStr.getBytes(), messageProperties);

            // 发送消息
            rabbitTemplate.send("stock-exchange", "stock-request-key", message, correlationData);

            return "Message sent successfully";
        } catch (Exception e) {
            e.printStackTrace();
            return "Failed to send message: " + e.getMessage();
        }
    }
}