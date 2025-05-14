package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.OutcomeDao;
import xjtu.dao.Outcome_DatasetDao;
import xjtu.pojo.Outcome_Dataset;
import xjtu.service.Outcome_DatasetService;

import java.util.List;

@Service
public class Outcome_DatasetImpl implements Outcome_DatasetService {
    @Autowired
    Outcome_DatasetDao outcomeDatasetDao;
    @Override
    public int addOutcome_Dataset(Outcome_Dataset outcome_dataset) {
        return this.outcomeDatasetDao.addOutcome_Dataset(outcome_dataset);
    }

    @Override
    public List<Outcome_Dataset> listAll() {
        return this.outcomeDatasetDao.listAll();
    }

    @Override
    public int removeById(int id) {
        return outcomeDatasetDao.removeById(id);
    }

    @Override
    public int updateById(Outcome_Dataset outcome_dataset, int id) {
        return 0;
    }
}
