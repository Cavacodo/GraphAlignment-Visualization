package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.Outcome;
import xjtu.pojo.User;
import xjtu.service.OutcomeService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/outcome")
public class OutcomeController {
    @Autowired
    OutcomeService outcomeService;
    @PostMapping("/getOutcomeByType")
    public List<Outcome> getOutcomeByType(@RequestBody Map<String,String> map)
    {
        return outcomeService.getEvaluationIndex(map.get("type"),map.get("user"),map.get("dataset"));
    }
}