package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import xjtu.annotation.Auth;
import xjtu.service.EmailService;

@RestController
public class EmailController {
    @Autowired
    private EmailService emailService;
    @RequestMapping("/sendEmail")
    public int sendEmail(String email) {
        emailService.send(email);
        return 1;
    }
}
