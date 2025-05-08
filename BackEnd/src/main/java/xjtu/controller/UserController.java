package xjtu.controller;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import xjtu.dao.RoleDao;
import xjtu.dao.RoleDictDao;
import xjtu.pojo.User;
import xjtu.pojo.utils.R;
import xjtu.pojo.utils.ResponseEnum;
import xjtu.pojo.utils.TokenUtil;
import xjtu.pojo.utils.UserWithRole;
import xjtu.service.RoleService;
import xjtu.service.UserService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/user")
public class UserController {
    @Autowired
    private UserService userService;

    @Autowired
    private RoleService roleService;


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
        return userService.addUserTransaction(user);
    }
    @GetMapping("/listUserWithPrivilege")
    @ResponseBody
    public List<UserWithRole> listUserWithPrivilege()
    {
        return userService.listUserWithPrivilege();
    }
    @PostMapping("/login")
    @ResponseBody
    public R<Map<String,String>> login(@RequestBody Map<String, String> credentials){
        String username = credentials.get("account");
        String pwd = credentials.get("pwd");
        Map<String,String> response = new HashMap<>();
        if(username.isBlank() || pwd.isBlank()){
            return R.error(ResponseEnum.USERNAME_PASSWORD_ERROR);
        }
        if(this.userService.login(username,pwd) == 1){
            String role = this.roleService.findRoleByAccount(username);
            String token = TokenUtil.createToken(username,role);
            response.put("token",token);
            response.put("role",role);
            response.put("account",username);
            return R.ok(response);
        }
        return R.error(ResponseEnum.USERNAME_PASSWORD_ERROR);
    }
    @PostMapping("/forgetPassword")
    @ResponseBody
    public ResponseEntity<String> forgetPassword(@RequestBody Map<String,String> info){
        String email = info.get("email");
        String pwd = info.get("password");
        String verifyCode = info.get("verifyCode");
        if(userService.findUserByEmail(email) == null) return new ResponseEntity<>("该邮箱未注册", HttpStatus.BAD_REQUEST);
        String vCode = userService.getRedisVerifyCode(email);
        if(vCode == null) return new ResponseEntity<>("验证码已过期", HttpStatus.ALREADY_REPORTED);
        if(!vCode.equals(verifyCode)) return new ResponseEntity<>("验证码错误", HttpStatus.CONFLICT);
        int userId = userService.findUserByEmail(email);
        userService.updatePwdById(userId,pwd);
        return new ResponseEntity<>("发送成功", HttpStatus.ACCEPTED);
    }
    @PostMapping("/register")
    @ResponseBody
    public ResponseEntity<String> register(@RequestBody Map<String,String> info){
        User user = new User(0,info.get("username"),info.get("password"),info.get("email"));
        String verifyCode = info.get("verifyCode");
        int res = userService.register(user,verifyCode);
        if(res == 1) return new ResponseEntity<>("发送成功", HttpStatus.ACCEPTED);
        else if(res == -1) return new ResponseEntity<>("该邮箱已被注册或者用户名重复", HttpStatus.CONFLICT);
        else return new ResponseEntity<>("发送失败", HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/getEmailByName")
    @ResponseBody
    public String getEmailByName(String name)
    {
        User userByAccount = userService.findUserByAccount(name);
        return userByAccount.getEmail();
    }

    @PostMapping("/changeUserPwd")
    @ResponseBody
    public ResponseEntity<String> changeUserPwd(@RequestBody Map<String, String> payload){
        String account = payload.get("account");
        String oldpwd = payload.get("oldpwd");
        String newpwd = payload.get("newpwd");
        int ans = this.userService.updatePassword(account, oldpwd, newpwd);
        if(ans == 1) return new ResponseEntity<>("修改成功", HttpStatus.ACCEPTED);
        return new ResponseEntity<>("修改失败", HttpStatus.BAD_REQUEST);
    }
}
