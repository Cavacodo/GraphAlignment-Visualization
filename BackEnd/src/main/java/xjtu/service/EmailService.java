package xjtu.service;
/**
 * @author heshi
 */

public interface EmailService {
    public void send(String email);
    public String getVerifyCode();
}