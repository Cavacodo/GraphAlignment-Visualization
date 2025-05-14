package xjtu.service;

import xjtu.pojo.Outcome_Dataset;

import java.util.List;

public interface Outcome_DatasetService {
    int addOutcome_Dataset(Outcome_Dataset outcome_dataset);
    List<Outcome_Dataset> listAll();
    int removeById(int id);
    int updateById(Outcome_Dataset outcome_dataset,int id);
}
