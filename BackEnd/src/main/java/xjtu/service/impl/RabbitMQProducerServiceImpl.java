package xjtu.service.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.service.RabbitMQProducerService;

@Service
public class RabbitMQProducerServiceImpl implements RabbitMQProducerService {

    @Autowired(required = false)
    private AmqpTemplate rabbitTemplate;

    @Override
    public void sendJsonMessage(Object jsonData) {
        try {
            String jsonStr = new ObjectMapper().writeValueAsString(jsonData);
            rabbitTemplate.convertAndSend("stock-exchange", "stock-key", jsonStr);
        } catch (Exception e) {
            // 处理异常
        }
    }
}

