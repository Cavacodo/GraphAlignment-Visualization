package xjtu.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;


@AllArgsConstructor
@NoArgsConstructor
@Data
public class Experiment {
    private Integer id;
    private String user_account;
    private Integer outcome_id;
    private LocalDateTime date;
}
