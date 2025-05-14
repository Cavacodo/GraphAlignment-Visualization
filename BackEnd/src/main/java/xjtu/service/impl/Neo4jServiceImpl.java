package xjtu.service.impl;

import cn.hutool.core.io.resource.ClassPathResource;
import cn.hutool.core.lang.hash.Hash;
import org.springframework.stereotype.Service;
import xjtu.pojo.Neo4j;
import xjtu.service.Neo4jService;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;

@Service
public class Neo4jServiceImpl implements Neo4jService {

    private List<List<Integer>> readFile(String file) throws Exception {
        List<List<Integer>> ans = new ArrayList<>();
        try {
            ClassPathResource resource = new ClassPathResource("static/" + file);
            BufferedReader reader = new BufferedReader(new InputStreamReader(resource.getStream(), "UTF-8"));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] tmp = line.split(" ");
                List<Integer> tmpList = new ArrayList<>();
                for (String s : tmp) {
                    tmpList.add(Integer.parseInt(s));
                }
                ans.add(tmpList);
            }
            return ans;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

    }
    @Override
    public List<List<Integer>> getInternalRelationship(String file) throws Exception {
        return readFile(file);
    }

    @Override
    public List<List<Integer>> getDoubanGroundTruth(int batch) throws Exception {
        List<List<Integer>> alignRelation = readFile("douban_ground_True.txt");
        // 按照src从小到大排序
        alignRelation.sort((o1, o2) -> o1.get(1) - o2.get(1));
        List<List<Integer>> ans =  new ArrayList<>();
        if(batch == 0){
            for(int i = 0 ; i < 300; i++) ans.add(alignRelation.get(i));
        }else if(batch == 1){
            for(int i = 300; i < 600; i++) ans.add(alignRelation.get(i));
        }else if(batch == 2){
            for(int i = 600; i < 900; i++) ans.add(alignRelation.get(i));
        }else if(batch == 3){
            for(int i = 900; i < alignRelation.size(); i++) ans.add(alignRelation.get(i));
        }
        return ans;
    }

    @Override
    public Neo4j getDoubanNode(int type, int k, int id) throws Exception{
        List<List<Integer>> offline = readFile("douban_s_edge.txt");
        List<List<Integer>> online = readFile("douban_t_edge.txt");
        List<List<Integer>> align = readFile("douban_ground_True.txt");
        HashSet<Integer> set = new HashSet<>();
        List<List<Integer>> src = new ArrayList<>();
        List<List<Integer>> target = new ArrayList<>();
        List<List<Integer>> alignRelation = new ArrayList<>();
        List<Integer> src_node = new ArrayList<>();
        List<Integer> target_node = new ArrayList<>();
        set.add(id);
        if(type == 0){
            for(int i = 0 ; i < k; i++){
                List<Integer> tmp = new ArrayList<>();
                for(int j = 0 ; j < offline.size(); j++){
                    if(set.contains(offline.get(j).get(0))) tmp.add(offline.get(j).get(1));
                    if(set.contains(offline.get(j).get(1))) tmp.add(offline.get(j).get(0));
                }
                for(int j = 0 ; j < tmp.size(); j++) set.add(tmp.get(j));
            }
            for(int i = 0 ; i < offline.size(); i++){
                if(set.contains(offline.get(i).get(0)) && set.contains(offline.get(i).get(1))){
                    src.add(offline.get(i));
                }
            }
            HashSet<Integer> target_set = new HashSet<>();
            // 找对齐节点
            for(int i = 0 ; i < align.size(); i++){
                if(set.contains(align.get(i).get(1))){
                    target_set.add(align.get(i).get(0));
                    alignRelation.add(align.get(i));
                }
            }
            // target网络节点
            for(int i = 0 ; i < online.size(); i++){
                if(target_set.contains(online.get(i).get(0)) && target_set.contains(online.get(i).get(1))) target.add(online.get(i));
            }
            for(Integer v : set) src_node.add(v);
            for(Integer v : target_set) target_node.add(v);
            return new Neo4j(src_node,target_node,src,target,alignRelation);
        }else if(type == 1){
            for(int i = 0 ; i < k; i++){
                List<Integer> tmp = new ArrayList<>();
                for(int j = 0 ; j < online.size(); j++){
                    if(set.contains(online.get(j).get(0))) tmp.add(online.get(j).get(1));
                    if(set.contains(online.get(j).get(1))) tmp.add(online.get(j).get(0));
                }
                for(int j = 0 ; j < tmp.size(); j++) set.add(tmp.get(j));
            }
            for(int i = 0 ; i < online.size(); i++){
                if(set.contains(online.get(i).get(0)) && set.contains(online.get(i).get(1))){
                    src.add(online.get(i));
                }
            }
            HashSet<Integer> target_set = new HashSet<>();
            // 找对齐节点
            for(int i = 0 ; i < align.size(); i++){
                if(set.contains(align.get(i).get(0))){
                    target_set.add(align.get(i).get(1));
                    alignRelation.add(align.get(i));
                }
            }
            // target网络节点
            for(int i = 0 ; i < offline.size(); i++){
                if(target_set.contains(offline.get(i).get(0)) && target_set.contains(offline.get(i).get(1))) target.add(offline.get(i));
            }
            for(Integer v : set) src_node.add(v);
            for(Integer v : target_set) target_node.add(v);
            return new Neo4j(src_node,target_node,src,target,alignRelation);
        }
        return null;
    }

    @Override
    public Neo4j getPPINode(int type, int k, int id) throws Exception {
        List<List<Integer>> offline = readFile("ppi_s_edge.txt");
        List<List<Integer>> online = readFile("ppi_t_edge.txt");
        List<List<Integer>> align = readFile("ppi_ground_True.txt");
        HashSet<Integer> set = new HashSet<>();
        List<List<Integer>> src = new ArrayList<>();
        List<List<Integer>> target = new ArrayList<>();
        List<List<Integer>> alignRelation = new ArrayList<>();
        List<Integer> src_node = new ArrayList<>();
        List<Integer> target_node = new ArrayList<>();
        set.add(id);
        if(type == 0){
            for(int i = 0 ; i < k; i++){
                List<Integer> tmp = new ArrayList<>();
                for(int j = 0 ; j < offline.size(); j++){
                    if(set.contains(offline.get(j).get(0))) tmp.add(offline.get(j).get(1));
                    if(set.contains(offline.get(j).get(1))) tmp.add(offline.get(j).get(0));
                }
                for(int j = 0 ; j < tmp.size(); j++) set.add(tmp.get(j));
            }
            for(int i = 0 ; i < offline.size(); i++){
                if(set.contains(offline.get(i).get(0)) && set.contains(offline.get(i).get(1))){
                    src.add(offline.get(i));
                }
            }
            HashSet<Integer> target_set = new HashSet<>();
            // 找对齐节点
            for(int i = 0 ; i < align.size(); i++){
                if(set.contains(align.get(i).get(1))){
                    target_set.add(align.get(i).get(0));
                    alignRelation.add(align.get(i));
                }
            }
            // target网络节点
            for(int i = 0 ; i < online.size(); i++){
                if(target_set.contains(online.get(i).get(0)) && target_set.contains(online.get(i).get(1))) target.add(online.get(i));
            }
            for(Integer v : set) src_node.add(v);
            for(Integer v : target_set) target_node.add(v);
            return new Neo4j(src_node,target_node,src,target,alignRelation);
        }else if(type == 1){
            for(int i = 0 ; i < k; i++){
                List<Integer> tmp = new ArrayList<>();
                for(int j = 0 ; j < online.size(); j++){
                    if(set.contains(online.get(j).get(0))) tmp.add(online.get(j).get(1));
                    if(set.contains(online.get(j).get(1))) tmp.add(online.get(j).get(0));
                }
                for(int j = 0 ; j < tmp.size(); j++) set.add(tmp.get(j));
            }
            for(int i = 0 ; i < online.size(); i++){
                if(set.contains(online.get(i).get(0)) && set.contains(online.get(i).get(1))){
                    src.add(online.get(i));
                }
            }
            HashSet<Integer> target_set = new HashSet<>();
            // 找对齐节点
            for(int i = 0 ; i < align.size(); i++){
                if(set.contains(align.get(i).get(0))){
                    target_set.add(align.get(i).get(1));
                    alignRelation.add(align.get(i));
                }
            }
            // target网络节点
            for(int i = 0 ; i < offline.size(); i++){
                if(target_set.contains(offline.get(i).get(0)) && target_set.contains(offline.get(i).get(1))) target.add(offline.get(i));
            }
            for(Integer v : set) src_node.add(v);
            for(Integer v : target_set) target_node.add(v);
            return new Neo4j(src_node,target_node,src,target,alignRelation);
        }
        return null;
    }

    @Override
    public List<List<Integer>> getPPIGroundTruth(int batch) throws Exception {
        List<List<Integer>> alignRelation = readFile("ppi_ground_True.txt");
        // 按照src从小到大排序
        alignRelation.sort((o1, o2) -> o1.get(1) - o2.get(1));
        List<List<Integer>> ans =  new ArrayList<>();
        if(batch == 0){
            for(int i = 0 ; i < 300; i++) ans.add(alignRelation.get(i));
        }else if(batch == 1){
            for(int i = 300; i < 600; i++) ans.add(alignRelation.get(i));
        }else if(batch == 2){
            for(int i = 600; i < 900; i++) ans.add(alignRelation.get(i));
        }else if(batch == 3){
            for(int i = 900; i < 1200; i++) ans.add(alignRelation.get(i));
        }else if(batch == 4){
            for(int i = 1200 ; i < 1500; i++) ans.add(alignRelation.get(i));
        }else if (batch == 5){
            for(int i = 1500 ; i < alignRelation.size(); i++) ans.add(alignRelation.get(i));
        }
        return ans;
    }
}
