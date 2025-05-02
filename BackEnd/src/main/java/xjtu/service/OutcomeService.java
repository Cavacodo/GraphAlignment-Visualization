package xjtu.service;

import xjtu.pojo.Outcome;

import java.util.List;

public interface OutcomeService {
    int addOutcome(Outcome outcome);
    List<Outcome> getOutcome();
    Integer getLastestId();
    Integer addEvaluationById(String evaluation,Integer id);
    List<Outcome> getEvaluationIndex(String index);
}
