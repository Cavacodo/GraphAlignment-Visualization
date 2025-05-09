package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.dao.RoleDao;
import xjtu.dao.RoleDictDao;
import xjtu.pojo.Role;
import xjtu.service.RoleService;

import java.util.List;

@Service
public class RoleServiceImpl implements RoleService {
    @Autowired
    RoleDao roleDao;

    @Autowired
    RoleDictDao roleDictDao;

    @Override
    public List<Role> listRole() {
        return roleDao.listRole();
    }

    @Override
    public String findRoleByAccount(String account) {
        Role roleByAccount = roleDao.findRoleByAccount(account);
        return this.roleDictDao.getRoleNameById(roleByAccount.getRole());
    }

    //返回1表示添加成功，0表示添加失败
    @Override
    public int addRole(Role role) {
        if(findRoleByAccount(role.getAccount()) == null){
            roleDao.addRole(role);
            return 1;
        }
        return 0;
    }

    @Override
    public int changeUserPrivilege(String account, int role) {
        // 如果权限非法，返回-1
        if(role < 0 || role > 2) return -1;
        // 如果用户不存在，返回0
        if(findRoleByAccount(account) == null) return 0;
        return roleDao.changeUserPrivilege(account, role);
    }

    @Override
    public List<Role> getRoleByCondition(String col, String key) {
        return this.roleDao.getRoleByCondition(col, key);
    }

    @Override
    public int removeRoleById(int id) {
        return this.roleDao.removeRoleById(id);
    }

    @Override
    public int updateRoleByAccount(Role role, String account) {
        return this.roleDao.updateRoleByAccount(role, account);
    }
}
