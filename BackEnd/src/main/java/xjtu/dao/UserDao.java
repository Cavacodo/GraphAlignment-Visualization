package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.query.UserQuery;
import xjtu.pojo.User;

import java.util.List;

@Mapper
@Repository
public interface UserDao {
    public List<User> listUser();
    public List<User> listUserByName(UserQuery userQuery);
}
