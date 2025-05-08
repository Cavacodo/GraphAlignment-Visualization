package xjtu.service;


import org.springframework.stereotype.Service;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;


import java.util.List;


public interface UserService {
    List<User> listUser();
    User findUserByAccount(String account);
    int checkAccountExistence(String account);
    int checkEmailDuplicate(String email);
    List<UserWithRole> listUserWithPrivilege();
    int login(String account, String pwd);
    int addUserTransaction(User user);
    Integer findUserByEmail(String email);
    String getRedisVerifyCode(String email);
    int updatePwdById(int id,String pwd);
    int register(User user, String verifyCode);
    String getRoleById(int id);
    int updatePassword(String account,String old,String newpwd);
}
