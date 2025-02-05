package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import xjtu.service.RabbitMQProducerService;

@Controller
@RequestMapping("/api")
public class RabbitMQController {

    @Autowired
    private RabbitMQProducerService rabbitMQProducerService;

    @PostMapping("/send")
    public String sendJsonMessage(@RequestBody Object jsonData) {
        rabbitMQProducerService.sendJsonMessage(jsonData);
        System.out.println(jsonData);
        return "JSON message sent to RabbitMQ!";
    }
}
