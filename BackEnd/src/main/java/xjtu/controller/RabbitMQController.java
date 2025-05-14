package xjtu.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;
import xjtu.pojo.Outcome_Dataset;
import xjtu.service.ExperimentService;
import xjtu.service.OutcomeService;
import xjtu.service.Outcome_DatasetService;
import xjtu.service.RabbitMQProducerService;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;

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

    @Autowired
    private OutcomeService outcomeService;
    @Autowired
    ExperimentService experimentService;

    @Autowired
    Outcome_DatasetService outcomeDatasetService;


    @PostMapping("/send")
    public ResponseEntity<String> sendJsonMessage(@RequestBody JSONObject jsonData) {
        rabbitMQProducerService.sendJsonMessage(jsonData);
        System.out.println(jsonData);
        this.outcomeService.addOutcome(new Outcome(0,jsonData.getString("type"),jsonData.getString("args"),null));
        String user = jsonData.getString("user");
        LocalDateTime date = LocalDateTime.now();
        int outcome_id = this.outcomeService.getLastestId();
        this.experimentService.addExperiment(new Experiment(0,user,outcome_id,date));
        int dataset = jsonData.getString("dataset").equals("douban") ? 1 : 2;
        this.outcomeDatasetService.addOutcome_Dataset(new Outcome_Dataset(0,outcome_id,dataset));
        return new ResponseEntity<>("send success", HttpStatus.OK);
    }
    @GetMapping("/getPythonResult")
    public ResponseEntity<Map<String,Object>> getPythonResult(){
        Map<String,Object> map = new HashMap<>();
        while (!redisTemplate.hasKey("type") || !redisTemplate.hasKey("acc") || !redisTemplate.hasKey("m") || !redisTemplate.hasKey("dataset")) ;
        String acc = (String) redisTemplate.opsForValue().get("acc");
        Map<String,String> tmap = new HashMap<>();
        String[] acc_s = acc.split(",");
        for(String s : acc_s){
            String[] s_s = s.split(":");
            tmap.put(s_s[0],s_s[1]);
        }
        map.put("dataset",redisTemplate.opsForValue().get("dataset"));
        map.put("type",redisTemplate.opsForValue().get("type"));
        map.put("acc",tmap);
        map.put("m",convertString2Array((String) redisTemplate.opsForValue().get("m")));
        redisTemplate.delete("dataset");
        redisTemplate.delete("type");
        redisTemplate.delete("acc");
        redisTemplate.delete("m");
        Integer id = this.outcomeService.getLastestId();
        if(id == null) return new ResponseEntity<>(map, HttpStatus.BAD_REQUEST);
        this.outcomeService.addEvaluationById(tmap.toString(),id);

        return new ResponseEntity<>(map, HttpStatus.OK);
    }
    public List<List<Integer>> convertString2Array(String s){
        String sb = new String("\\], \\[");
        String[] tmp = s.split(sb);
        List<List<Integer>> ans = new ArrayList<>();
        for(int i = 0 ; i < tmp.length; i++){
            if(i == 0){
                tmp[i] = tmp[i].substring(2, tmp[i].length());
            }
            if(i == tmp.length - 1){
                tmp[i] = tmp[i].substring(0, tmp[i].length() - 2);
            }
            String[] tmp2 = tmp[i].split(", ");
            List<Integer> int_tmp = new ArrayList<>();
            for(String s2 : tmp2){
                int_tmp.add(Integer.parseInt(s2));
            }
            ans.add(int_tmp);
        }
        return ans;
    }
}
