package xjtu.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import xjtu.service.RabbitMQProducerService;

import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Controller
@RequestMapping("/api")
public class RabbitMQController {

    @Autowired
    private RabbitMQProducerService rabbitMQProducerService;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private ObjectMapper objectMapper;


    @PostMapping("/send")
    public ResponseEntity<String> sendJsonMessage(@RequestBody Object jsonData) {

        rabbitMQProducerService.sendJsonMessage(jsonData);
        System.out.println(jsonData);

        while (true) {
            Map<String, String> map = objectMapper.convertValue(jsonData, Map.class);
            String val = map.get("type");
            List<Object> value = redisTemplate.opsForList().range("type", 0, -1);
            if (value != null) {
                return new ResponseEntity<>(""+value, HttpStatus.OK);
            }
            try {
                // Sleep for a short period before polling again
                TimeUnit.SECONDS.sleep(5);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new ResponseEntity<>("Polling interrupted", HttpStatus.INTERNAL_SERVER_ERROR);
            }
        }
    }
}
