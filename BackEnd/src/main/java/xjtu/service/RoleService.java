package xjtu.service;

import xjtu.pojo.Role;

import java.util.List;

public interface RoleService {
    List<Role> listRole();
    String findRoleByAccount(String account);
    int addRole(Role role);
    int changeUserPrivilege(String account, int role);
    List<Role> getRoleByCondition(String col, String key);
    int removeRoleById(int id);
    int updateRoleByAccount(Role role, String account);
}
