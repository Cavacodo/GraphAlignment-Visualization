package xjtu.controller;

import ch.qos.logback.core.util.StringUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import io.micrometer.common.util.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import xjtu.pojo.User;
import xjtu.pojo.utils.R;
import xjtu.pojo.utils.ResponseEnum;
import xjtu.pojo.utils.TokenUtil;
import xjtu.pojo.utils.UserWithRole;
import xjtu.service.TokenService;
import xjtu.service.UserService;

import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/user")
public class UserController {
    @Autowired
    private UserService userService;
    @Autowired
    private TokenService tokenService;
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
    public R<String> login(@RequestBody Map<String, String> credentials){
        String account = credentials.get("account");
        String pwd = credentials.get("pwd");
        if(StringUtils.isNotBlank(account) && StringUtils.isNotBlank(pwd)){
            if(userService.login(account,pwd) == 1 && tokenService.getTokenByAccount(account) == null){
                JSONObject jsonObject = JSONUtil.createObj().put("name","Me");
                String token = TokenUtil.createToken(jsonObject);
                tokenService.setToken(account,token);
                String data = tokenService.getTokenByAccount(account);
                return R.ok(data);
            }else if(userService.login(account,pwd) == 1 && tokenService.getTokenByAccount(account) != null){
                String token = tokenService.getTokenByAccount(account);
                if(TokenUtil.verifyToken(token)){
                    return R.ok(token);
                }else{
                    JSONObject jsonObject = JSONUtil.createObj().put("name","Me");
                    String newToken = TokenUtil.createToken(jsonObject);
                    tokenService.setToken(account,newToken);
                    String data = tokenService.getTokenByAccount(account);
                    return R.ok(data);
                }
            }
        }
        return R.error(ResponseEnum.USERNAME_PASSWORD_ERROR);
    }

}
