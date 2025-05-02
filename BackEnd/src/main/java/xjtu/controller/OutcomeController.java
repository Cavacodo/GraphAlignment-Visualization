package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.Outcome;
import xjtu.service.OutcomeService;

import java.util.List;

@RestController
@RequestMapping("/outcome")
public class OutcomeController {
    @Autowired
    OutcomeService outcomeService;
    @PostMapping("/getOutcomeByType")
    public List<Outcome> getOutcomeByType(@RequestParam String type)
    {
        return outcomeService.getEvaluationIndex(type);
    }
}
