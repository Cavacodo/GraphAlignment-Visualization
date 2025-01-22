package xjtu.service;

import xjtu.pojo.Role;

import java.util.List;

public interface RoleService {
    List<Role> listRole();
    Role findRoleByAccount(String account);
    int addRole(Role role);
    int changeUserPrivilege(String account, int role);
}
