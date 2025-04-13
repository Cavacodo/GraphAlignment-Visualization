package xjtu.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Neo4j {
    private List<Integer> src_node;
    private List<Integer> target_node;
    private List<List<Integer>> src;
    private List<List<Integer>> target;
    private List<List<Integer>> align;
}
