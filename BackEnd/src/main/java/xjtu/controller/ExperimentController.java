package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;
import xjtu.service.ExperimentService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/exp")
public class ExperimentController {
    @Autowired
    ExperimentService experimentService;
    @GetMapping("/getExpByAccount")
    @ResponseBody
    public List<Outcome> getExpByAccount(String account,String alg,String dataset) {
        return experimentService.getExperimentByUser(account,alg,dataset);
    }

    @PostMapping("/removeExpByOutcomeId")
    @ResponseBody
    public int removeExpByOutcomeId(@RequestBody Map<String,String> map) {
        return experimentService.removeExperimentByOutcomeId(Integer.parseInt(map.get("id")));
    }

}
