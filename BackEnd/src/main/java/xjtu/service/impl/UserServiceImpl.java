package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import xjtu.annotation.Auth;
import xjtu.dao.RoleDao;
import xjtu.dao.TokenDao;
import xjtu.dao.UserDao;
import xjtu.pojo.Role;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;
import xjtu.service.TokenService;
import xjtu.service.UserService;

import java.util.List;
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserDao userDao;
    @Autowired
    RoleDao roleDao;
    @Autowired
    TokenDao tokenDao;
    @Override
    public List<User> listUser() {
        return userDao.listUser();
    }

    @Override
    public User findUserByAccount(String account) {
        return userDao.findUserByAccount(account);
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

    @Override
    public int login(String account, String pwd) {
        if(findUserByAccount(account) == null) return -1;
        return userDao.login(account,pwd);
    }

    @Transactional
    @Override
    public int addUserTransaction(User user) {
        int userAdd = userDao.addUser(user);
        int roleAdd = roleDao.addRole(new Role(0,user.getAccount(), 1));
        int tokenAdd = tokenDao.addToken(user.getAccount(), "");
        return userAdd + roleAdd + tokenAdd;
    }
}
