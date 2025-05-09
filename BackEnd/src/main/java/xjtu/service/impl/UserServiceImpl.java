package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import xjtu.dao.RoleDao;
import xjtu.dao.RoleDictDao;
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
    RoleDao roleDao;
    @Autowired
    RoleDictDao roleDictDao;
    private final RedisTemplate<String,Object> redisTemplate;

    @Autowired
    public UserServiceImpl(RedisTemplate<String, Object> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

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
    public String getRoleById(int id){
        return this.roleDictDao.getRoleNameById(id);
    }

    @Override
    public int updatePassword(String account,String old, String newpwd) {

        return this.userDao.updatePwdByAccount(account,old,newpwd);
    }

    @Override
    public int updateEmailById(int id, String email) {
        return this.userDao.updateEmailById(id,email);
    }

    @Override
    public List<User> listAll() {
        return this.userDao.listAll();
    }

    @Override
    public List<User> findUserByCondition(String col, String key) {
        return this.userDao.findUserByCondition(col, key);
    }

    @Override
    public int removeUserById(int id) {
        return this.userDao.removeUserById(id);
    }

    @Override
    public int updateUserByAccount(User user, String account) {
        return this.userDao.updateUserByAccount(user,account);
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
        return userAdd + roleAdd;
    }

    @Override
    public Integer findUserByEmail(String email) {
        return userDao.findUserByEmail(email);
    }

    @Override
    public String getRedisVerifyCode(String email) {
        return (String) redisTemplate.opsForValue().get(email);
    }

    @Override
    public int updatePwdById(int id, String pwd) {
        return userDao.updatePwdById(id,pwd);
    }

    @Override
    public int register(User user, String verifyCode) {
        if(redisTemplate.opsForValue().get(user.getEmail()) == null || !verifyCode.equals(redisTemplate.opsForValue().get(user.getEmail()))) return -1;
        int res = addUserTransaction(user);
        if(res == 3){
            return 1;
        }
        return 0;
    }

}
