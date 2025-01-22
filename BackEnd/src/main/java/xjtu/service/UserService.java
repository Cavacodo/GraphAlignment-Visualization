package xjtu.service;

import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;


import java.util.List;


public interface UserService {
    List<User> listUser();
    User findUserByAccount(String account);
    int addUser(User user);
    int checkAccountExistence(String account);
    int checkEmailDuplicate(String email);
    List<UserWithRole> listUserWithPrivilege();
}
