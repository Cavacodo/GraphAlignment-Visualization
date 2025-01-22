package xjtu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import xjtu.annotation.Auth;

@RestController
@RequestMapping("/")
public class helloController {
    @Auth
    @PostMapping("/hello")
    public String hello()
    {
        return "hello";
    }
    @PostMapping("/hi")
    public String hi()
    {
        return "hi";
    }
}
