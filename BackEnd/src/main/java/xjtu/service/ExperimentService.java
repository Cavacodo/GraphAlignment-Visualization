package xjtu.service;

import org.springframework.stereotype.Service;
import xjtu.pojo.Experiment;
import xjtu.pojo.Outcome;

import java.util.List;

public interface ExperimentService {
    List<Outcome> listExperiment();
    List<Outcome> getExperimentByUser(String account);
    int addExperiment(Experiment experiment);
    int removeExperimentByOutcomeId(Integer id);
    List<Experiment> listAll();
    List<Experiment> getExpByCondition(String col,String key);
    int removeExperimentById(Integer id);
    int updateExperimentById(Experiment experiment,Integer id);
}
