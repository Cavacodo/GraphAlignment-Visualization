package xjtu.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.core.io.ClassPathResource;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/neo4j")
public class GroundTruthController {
    
    public List<List<Integer>> readFileToArray(String fileName) throws IOException {
        ClassPathResource resource = new ClassPathResource("static/" + fileName);
        InputStream inputStream = resource.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        List<List<Integer>> lines = new ArrayList<>();
        String line;
        List<Integer> src = new ArrayList<>();
        List<Integer> target = new ArrayList<>();
        lines.add(src);
        lines.add(target);
        while ((line = reader.readLine()) != null) {
            String[] tmp = line.split(" ");
            src.add(Integer.parseInt(tmp[1]));
            target.add(Integer.parseInt(tmp[0]));
        }
        return lines;
    }
    @GetMapping("/doubanGT")
    public List<List<Integer>> getDoubanGroundTruth() throws IOException {
        List<List<Integer>> nums = readFileToArray("douban_ground_True.txt");

        return nums;
    }

}
