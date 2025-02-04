package xjtu.service.impl;

import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import xjtu.pojo.utils.EmailUtil;
import xjtu.service.EmailService;

import java.security.GeneralSecurityException;
import java.time.Duration;

@Service
public class EmailServiceImpl implements EmailService {
    private final RedisTemplate<String, Object> redisTemplate;

    public EmailServiceImpl(RedisTemplate<String, Object> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public String send(String email) {
        Boolean b = redisTemplate.hasKey(email);
        if(b){
            return "邮件已经发出，请注意查收";
        }else {
            String emailCode = getVerifyCode();
            try {
                EmailUtil.sendMail(email, emailCode);
                redisTemplate.opsForValue().set(email, emailCode, Duration.ofMinutes(5));
                return emailCode;
            } catch (GeneralSecurityException e) {
                throw new RuntimeException(e);
            }
        }
    }

    @Override
    public String getVerifyCode() {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < 6; i++) {
            int code = (int) (Math.random() * 10);
            builder.append(code);
        }
        return builder.toString();
    }
}
