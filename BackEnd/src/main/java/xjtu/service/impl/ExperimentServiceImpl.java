package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.ExperimentDao;
import xjtu.dao.OutcomeDao;
import xjtu.dao.Outcome_DatasetDao;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;
import xjtu.pojo.Outcome_Dataset;
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

    @Autowired
    Outcome_DatasetDao outcomeDatasetDao;
    @Override
    public List<Outcome> listExperiment() {
        return null;
    }

    @Override
    public List<Outcome> getExperimentByUser(String account,String alg, String dataset) {
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
        List<Outcome> n_ans = new ArrayList<>();
        if(alg == null && dataset == null) return ans;
        else{
            if(alg != null && dataset != null){
                Integer d = dataset.equals("douban") ? 1 : 2;
                for(Outcome outcome : ans){
                    if(this.outcomeDatasetDao.getDatasetByOutcomeId(outcome.getId()) == d && outcome.getType().equalsIgnoreCase(alg)){
                        n_ans.add(outcome);
                    }
                }
                return n_ans;
            }else if(alg != null && dataset == null){
                for(Outcome outcome : ans){
                    if(this.outcomeDatasetDao.getDatasetByOutcomeId(outcome.getId()) == null) continue;
                    Integer tmp = this.outcomeDatasetDao.getDatasetByOutcomeId(outcome.getId());
                    if(this.outcomeDatasetDao.getDatasetByOutcomeId(outcome.getId()) == 1 && outcome.getType().equalsIgnoreCase(alg)){
                        n_ans.add(outcome);
                    }
                }
                return n_ans;
            }else if(alg == null && dataset != null){
                int d = dataset.equals("douban") ? 1 : 2;
                List<Integer> nums = this.outcomeDatasetDao.getOutcomeIdByDataset(d);
                for(Outcome outcome : ans){
                    if(nums.contains(outcome.getId())) n_ans.add(outcome);
                }
                return n_ans;
            }
        }
        return null;
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
