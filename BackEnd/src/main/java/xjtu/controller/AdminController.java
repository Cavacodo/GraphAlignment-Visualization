package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.Outcome;
import xjtu.pojo.Role;
import xjtu.pojo.User;
import xjtu.service.OutcomeService;
import xjtu.service.RoleService;
import xjtu.service.UserService;

import java.util.Map;

@Controller
@RequestMapping("/all")
public class AdminController {
    @Autowired
    UserService userservice;
    @Autowired
    RoleService roleService;
    @Autowired
    OutcomeService outcomeService;

    @GetMapping("/list")
    @ResponseBody
    public Object search(String table,String col,String key){
        if(col == null && key == null) return this.userservice.listUser();
        else{
            if(table.equalsIgnoreCase("user")){
                if(col.equalsIgnoreCase("all")) return this.userservice.listUser();
                return this.userservice.findUserByCondition(col,key);
            }else if(table.equalsIgnoreCase("outcome")){
                if(col.equalsIgnoreCase("all")) return this.outcomeService.listOutCome();
                return this.outcomeService.getOutComeByCondition(col,key);
            }else if(table.equalsIgnoreCase("role")){
                if(col.equalsIgnoreCase("all")) return this.roleService.listRole();
                return this.roleService.getRoleByCondition(col,key);
            }
        }
        return null;
    }

    @PostMapping("/delete")
    @ResponseBody
    public int delete(@RequestBody Map<String, Object> params) {
        String table = (String) params.get("table");
        Integer id = (Integer) params.get("id");
        System.out.println("Table: " + table);
        System.out.println("ID: " + id);

        if ("user".equalsIgnoreCase(table)) {
            return this.userservice.removeUserById(id);
        } else if ("outcome".equalsIgnoreCase(table)) {
            return this.outcomeService.removeOutcomeById(id);
        } else if ("role".equalsIgnoreCase(table)) {
            return this.roleService.removeRoleById(id);
        }
        return 0;
    }
    @PostMapping("/update")
    @ResponseBody
    public int update(@RequestBody Map<String, Object> params) {
        String table = (String) params.get("table");
        if(table.equalsIgnoreCase("user")){
            String account = (String) params.get("account");
            String password = (String) params.get("pwd");
            String email = (String) params.get("email");
            User user = new User(1,account,password,email);
            return this.userservice.updateUserByAccount(user,account);
        }else if(table.equalsIgnoreCase("role")){
            String account = (String) params.get("account");
            Integer role = (Integer) params.get("role");
            Role r= new Role(1,account,role);
            return this.roleService.updateRoleByAccount(r,account);
        }else if(table.equalsIgnoreCase("outcome")){
            Integer id = (Integer) params.get("id");
            String evaluation = (String) params.get("evaluation");
            String args = (String) params.get("args");
            String type = (String) params.get("type");
            Outcome outcome = new Outcome(id,type,args,evaluation);
            return this.outcomeService.updateOutcomeById(outcome,id);
        }
        return 0;
    }
}
