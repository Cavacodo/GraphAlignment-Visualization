package xjtu.service.impl;

import org.springframework.stereotype.Service;
import xjtu.pojo.utils.EmailUtil;
import xjtu.service.EmailService;

import java.security.GeneralSecurityException;

@Service
public class EmailServiceImpl implements EmailService {
    @Override
    public void send(String email) {
        String emailCode = getVerifyCode();
        try {
            EmailUtil.sendMail(email,emailCode);
        } catch (GeneralSecurityException e) {
            throw new RuntimeException(e);
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
