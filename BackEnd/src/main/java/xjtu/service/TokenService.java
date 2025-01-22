package xjtu.service;

public interface TokenService {
    String getTokenByAccount(String account);
    int setToken(String account,String token);
    int deleteToken(String account);
}
