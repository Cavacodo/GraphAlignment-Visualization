package xjtu.controller;

import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.User;
import xjtu.pojo.utils.UserWithRole;
import xjtu.service.UserService;

import java.util.List;

@Controller
public class UserController {
    @Autowired
    private UserService userService;
    @GetMapping("/listUser")
    @ResponseBody
    public List<User> listUser()
    {
        return userService.listUser();
    }

    @GetMapping("/findUserByAccount")
    @ResponseBody
    public User findUserByAccount(String account)
    {
        return userService.findUserByAccount(account);
    }
    @PostMapping("/addUser")
    @ResponseBody
    public int addUser(User user)
    {
        return userService.addUser(user);
    }
    @GetMapping("/listUserWithPrivilege")
    @ResponseBody
    public List<UserWithRole> listUserWithPrivilege()
    {
        return userService.listUserWithPrivilege();
    }
}
