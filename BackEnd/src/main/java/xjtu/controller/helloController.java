package xjtu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/")
public class helloController {
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
