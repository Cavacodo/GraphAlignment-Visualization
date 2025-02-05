package xjtu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import xjtu.annotation.Auth;
import xjtu.service.EmailService;

import java.util.Map;

@RestController
public class EmailController {
    @Autowired
    private EmailService emailService;
    @RequestMapping("/sendEmail")
    public ResponseEntity<String> sendEmail(@RequestBody Map<String,String> email) {
        try{
            String s = emailService.send(email.get("email"));
            if(s.equals("邮件已经发出，请注意查收")) return  new ResponseEntity<>(s, HttpStatus.ALREADY_REPORTED);
            else return new ResponseEntity<>("发送成功", HttpStatus.ACCEPTED);
        }catch (Exception e){
            return new ResponseEntity<>("发送失败", HttpStatus.BAD_REQUEST);
        }
    }
}
