package xjtu.service;
/**
 * @author heshi
 */

public interface EmailService {
    public String send(String email);
    public String getVerifyCode();
}