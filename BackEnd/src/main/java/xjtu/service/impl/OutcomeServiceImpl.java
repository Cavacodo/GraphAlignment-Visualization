package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.OutcomeDao;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;
import xjtu.service.ExperimentService;
import xjtu.service.OutcomeService;

import java.util.ArrayList;
import java.util.List;

@Service
public class OutcomeServiceImpl implements OutcomeService {
    @Autowired
    private OutcomeDao outcomeDao;
    @Autowired
    private ExperimentService experimentService;
    @Override
    public int addOutcome(Outcome outcome) {
        return this.outcomeDao.addOutcome(outcome);
    }

    @Override
    public List<Outcome> getOutcome() {
        return this.outcomeDao.getOutcome();
    }

    @Override
    public Integer getLastestId() {
        List<Outcome> outcome = this.outcomeDao.getLatest();
        if(outcome == null || outcome.size() > 1 || outcome.get(0).getEvaluation() != null) return null;
        Outcome res = outcome.get(0);
        return res.getId();
    }

    @Override
    public Integer addEvaluationById(String evaluation, Integer id) {
        return this.outcomeDao.addEvaluationById(evaluation,id);
    }

    @Override
    public List<Outcome> getEvaluationIndex(String index,String user){
        List<Outcome> outcomes  = this.experimentService.getExperimentByUser(user);
        List<Outcome> ans = new ArrayList<>();
        for(Outcome outcome : outcomes){
            String evaluation = outcome.getEvaluation();
            String[] tmp = evaluation.replaceAll("^\\{\\s*|\\s*\\}$", "").trim().split(", ");
            String t = new String();
            for(int i = 0; i < tmp.length; i++){
                String tmp_str = tmp[i].trim().replace("'","");
                if(tmp_str.contains(index)){
                    String[] strs = tmp_str.split("=");
                    t = strs[1].trim();
                }
            }
            outcome.setEvaluation(t);
            ans.add(outcome);
        }
        return ans;
    }

    @Override
    public List<Outcome> listOutCome() {
        return this.outcomeDao.listOutCome();
    }

    @Override
    public List<Outcome> getOutComeByCondition(String col, String key) {
        return this.outcomeDao.getOutComeByCondition(col,key);
    }

    @Override
    public int removeOutcomeById(Integer id) {
        return this.outcomeDao.removeOutcomeById(id);
    }

    @Override
    public int updateOutcomeById(Outcome outcome, Integer id) {
        return this.outcomeDao.updateOutcomeById(outcome,id);
    }

}
