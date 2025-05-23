package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.Role;

import java.util.List;

@Mapper
@Repository
public interface RoleDao {
    public List<Role> listRole();
    public Role findRoleByAccount(String account);
    public int addRole(Role role);
    public int changeUserPrivilege(String account, int role);
    public List<Role> getRoleByCondition(String col, String key);
    public int removeRoleById(int id);
    public int updateRoleByAccount(Role role, String account);
}
