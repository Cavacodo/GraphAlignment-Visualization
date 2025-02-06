package xjtu.controller;

import org.apache.ibatis.annotations.ResultMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/res")
public class PythonResultController {
    @Autowired
    private RedisTemplate redisTemplate;

    @RequestMapping("/python")
    public ResponseEntity<String> pythonResult(@RequestBody Map<String,Object> res)
    {
        System.out.println(res);
        String r = res.get("res").toString();
        redisTemplate.opsForValue().set("pyres",r);
        return ResponseEntity.ok(r);
    }

    @RequestMapping("/getRes")
    public ResponseEntity<String> getRes()
    {
        String r = redisTemplate.opsForValue().get("pyres").toString();
        return ResponseEntity.ok(r);
    }
}
