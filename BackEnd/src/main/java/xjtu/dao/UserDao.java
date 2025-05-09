package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;

import java.util.List;

@Mapper
@Repository
public interface UserDao {
    public List<User> listUser();
    public User findUserByAccount(String account);
    public int addUser(User user);
    public User checkEmailDuplicate(String email);
    public List<UserWithRole> listUserWithPrivilege();
    public int login(String account, String pwd);
    public Integer findUserByEmail(String email);
    public int updatePwdById(int id,String pwd);
    public int updatePwdByAccount(String account,String old,String newpwd);
    public int updateEmailById(int id,String email);
    public List<User> listAll();
    public List<User> findUserByCondition(String col,String key);
    public int removeUserById(int id);
    public int updateUserByAccount(User user,String account);
}
