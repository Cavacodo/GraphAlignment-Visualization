package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.core.io.ClassPathResource;
import xjtu.annotation.Auth;
import xjtu.pojo.Neo4j;
import xjtu.service.Neo4jService;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;

@RestController
@RequestMapping("/neo4j")
public class Neo4jController {
    @Autowired
    private Neo4jService neo4jService;
    @GetMapping("/doubanGT")
    public List<List<Integer>> getDoubanGroundTruth(int batch) throws Exception {
        return this.neo4jService.getDoubanGroundTruth(batch);
    }

    @GetMapping("/doubanInternal")
    public List<List<Integer>> getDoubanInternalRelationship(int type) throws Exception {
        String file = type == 0 ? "douban_s_edge.txt" : "douban_t_edge.txt";
        return this.neo4jService.getInternalRelationship(file);
    }
    @GetMapping("/doubanNetWork")
    public Neo4j getDoubanNetWork(int type,int k,int id) throws Exception {
        return this.neo4jService.getDoubanNode(type,k,id);
    }

}
