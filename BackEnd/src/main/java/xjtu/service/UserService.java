package xjtu.service;

import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;
import xjtu.pojo.User;
import xjtu.pojo.query.UserQuery;

import java.util.List;


public interface UserService {
    List<User> listUser();
}
