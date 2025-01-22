package xjtu.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.UserDao;
import xjtu.pojo.Role;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;
import xjtu.service.UserService;

import java.util.List;
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserDao userDao;
    @Autowired
    RoleServiceImpl roleServiceImpl;
    @Override
    public List<User> listUser() {
        return userDao.listUser();
    }

    @Override
    public User findUserByAccount(String account) {
        return userDao.findUserByAccount(account);
    }

    @Override
    public int addUser(User user) {
        System.out.println(checkEmailDuplicate(user.getEmail()) == 0);
        if(checkAccountExistence(user.getAccount()) == 1 && checkEmailDuplicate(user.getEmail()) == 1){
            if(roleServiceImpl.findRoleByAccount(user.getAccount()) != null) return 2;
            userDao.addUser(user);
            roleServiceImpl.addRole(new Role(0,user.getAccount(), 0));
            return 1;
        }
        else if(checkEmailDuplicate(user.getEmail()) == 0) return 0;
        return -1;
    }

    @Override
    public int checkAccountExistence(String account) {
        User res = userDao.findUserByAccount(account);
        if(res == null) return 1;
        return 0;
    }

    @Override
    public int checkEmailDuplicate(String email) {
        User res = userDao.checkEmailDuplicate(email);
        if(res == null) return 1;
        return 0;
    }

    @Override
    public List<UserWithRole> listUserWithPrivilege() {
        return userDao.listUserWithPrivilege();
    }

}
