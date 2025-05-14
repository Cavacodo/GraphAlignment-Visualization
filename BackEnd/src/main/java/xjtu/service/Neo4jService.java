package xjtu.service;

import java.util.List;
import xjtu.pojo.Neo4j;

public interface Neo4jService {
    List<List<Integer>> getInternalRelationship(String file) throws Exception;
    List<List<Integer>> getDoubanGroundTruth(int batch) throws Exception;
    Neo4j getDoubanNode(int type,int k,int id) throws Exception;
    Neo4j getPPINode(int type,int k,int id) throws Exception;
    List<List<Integer>> getPPIGroundTruth(int batch) throws Exception;
}
