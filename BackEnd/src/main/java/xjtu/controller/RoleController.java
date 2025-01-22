package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import xjtu.pojo.Role;
import xjtu.service.RoleService;

import java.util.List;

@Controller
public class RoleController {
    @Autowired
    private RoleService roleService;

    @GetMapping("/listRole")
    @ResponseBody
    public List<Role> listRole() {
        return roleService.listRole();
    }
    @GetMapping("/findRoleByAccount")
    @ResponseBody
    public Role findRoleByAccount(String account) {
        return roleService.findRoleByAccount(account);
    }
    @PostMapping("/changeUserPrivilege")
    @ResponseBody
    public int changeUserPrivilege(String account, int role) {
        return roleService.changeUserPrivilege(account, role);
    }
}
