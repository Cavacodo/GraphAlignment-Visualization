package xjtu.pojo.utils;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import xjtu.pojo.User;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserWithRole {
    private int id;
    private String account;
    private String pwd;
    private String email;
    private int role;
}
