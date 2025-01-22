package xjtu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import xjtu.pojo.utils.R;
import xjtu.pojo.utils.ResponseEnum;

@RestController
@RequestMapping("/error")
public class ErrorController {
    @PostMapping("/token")
    public R<?> token(){
        return R.error(ResponseEnum.NO_TOKEN);
    }
    @PostMapping("/tokenError")
    public R<?> tokenError(){
        return R.error(ResponseEnum.TOKEN_VERIFY_ERROR);
    }
}
