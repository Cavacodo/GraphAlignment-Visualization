package xjtu.service;

import org.springframework.stereotype.Service;
import xjtu.pojo.User;

import java.util.List;


public interface UserService {
    List<User> listUser();
}
