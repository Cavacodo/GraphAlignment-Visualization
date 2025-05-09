package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.Outcome;

import java.util.List;

@Mapper
@Repository
public interface OutcomeDao {
    public int addOutcome(Outcome outcome);
    public List<Outcome> getOutcome();
    public int addEvaluationById(String evaluation,Integer id);
    public List<Outcome> getLatest();
    public List<Outcome> listOutCome();
    public List<Outcome> getOutComeByCondition(String col,String key);
    public int removeOutcomeById(Integer id);
    public int updateOutcomeById(Outcome outcome,Integer id);
}
