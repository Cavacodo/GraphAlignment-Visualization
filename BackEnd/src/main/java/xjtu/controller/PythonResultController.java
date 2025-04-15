package xjtu.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.ibatis.annotations.ResultMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/res")
public class PythonResultController {
    @Autowired
    private RedisTemplate redisTemplate;
    @Autowired
    private ObjectMapper objectMapper;

    @RequestMapping("/python")
    public ResponseEntity<String> pythonResult(@RequestBody Map<String,Object> res)
    {
        System.out.println(res);
        String type = (String) res.get("type");
        String acc = (String) res.get("acc");
        List<Object> m = (List<Object>) res.get("m");
        if(type == null) return new ResponseEntity<>("type is null", HttpStatus.BAD_REQUEST);
        redisTemplate.opsForList().rightPush("type",type);
        return new ResponseEntity<>("done", HttpStatus.OK);
    }
}
