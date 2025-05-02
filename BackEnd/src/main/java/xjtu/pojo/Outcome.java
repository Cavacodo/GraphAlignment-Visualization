package xjtu.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class Outcome {
    private int id;
    private String type;
    private String args;
    private String evaluation;
}
