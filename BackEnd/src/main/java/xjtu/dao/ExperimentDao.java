package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.Experiment;

import java.util.List;

@Repository
@Mapper
public interface ExperimentDao {
    List<Experiment> listExperiment();
    List<Experiment> getExperimentByUser(String account);
    int addExperiment(Experiment experiment);
    int removeExperimentByOutcomeId(Integer outcome_id);
    List<Experiment> getExpByCondition(String col,String key);
    int removeExperimentById(Integer id);
    int updateExperimentById(Experiment experiment,Integer id);
}
