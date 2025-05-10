package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.ExperimentDao;
import xjtu.dao.OutcomeDao;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;
import xjtu.service.ExperimentService;
import xjtu.service.OutcomeService;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

@Service
public class ExperimentServiceImpl implements ExperimentService {
    @Autowired
    ExperimentDao experimentDao;
    @Autowired
    OutcomeDao outcomeDao;
    @Override
    public List<Outcome> listExperiment() {
        return null;
    }

    @Override
    public List<Outcome> getExperimentByUser(String account) {
        List<Outcome> outcomes = this.outcomeDao.getOutcome();
        List<Experiment> experimentByUser = this.experimentDao.getExperimentByUser(account);
        HashSet<Integer> set = new HashSet<>();
        for(Experiment experiment : experimentByUser){
            set.add(experiment.getOutcome_id());
        }
        List<Outcome> ans = new ArrayList<>();
        for(Outcome outcome : outcomes){
            if(set.contains(outcome.getId())){
                ans.add(outcome);
            }
        }
        return ans;
    }

    @Override
    public int addExperiment(Experiment experiment) {
        return this.experimentDao.addExperiment(experiment);
    }

    @Override
    public int removeExperimentByOutcomeId(Integer id) {
        return this.experimentDao.removeExperimentByOutcomeId(id);
    }

    @Override
    public List<Experiment> listAll() {
        return this.experimentDao.listExperiment();
    }

    @Override
    public List<Experiment> getExpByCondition(String col, String key) {
        return this.experimentDao.getExpByCondition(col,key);
    }

    @Override
    public int removeExperimentById(Integer id) {
        return this.experimentDao.removeExperimentById(id);
    }

    @Override
    public int updateExperimentById(Experiment experiment, Integer id) {
        return this.experimentDao.updateExperimentById(experiment,id);
    }
}
