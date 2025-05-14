package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.Outcome_Dataset;

import java.util.List;

@Mapper
@Repository
public interface Outcome_DatasetDao {
    int addOutcome_Dataset(Outcome_Dataset outcome_dataset);
    List<Outcome_Dataset> listAll();
    Integer getDatasetByOutcomeId(int id);
    List<Integer> getOutcomeIdByDataset(int dataset);
    int removeById(int id);
}
