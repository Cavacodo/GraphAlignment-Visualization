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
}
