package xjtu.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import xjtu.annotation.Auth;
import xjtu.dao.TokenDao;
import xjtu.service.TokenService;
@Service
public class TokenServiceImpl implements TokenService {
    @Autowired
    TokenDao tokenDao;
    @Override
    public String getTokenByAccount(String account) {
        return tokenDao.getTokenByAccount(account);
    }

    @Override
    public int setToken(String account, String token) {
        if(tokenDao.setToken(account,token)==1)
            return 1;
        return 0;
    }

    @Override
    public int deleteToken(String account) {
        return tokenDao.deleteToken(account);
    }

    @Override
    public int addToken(String account, String token) {
        return tokenDao.addToken(account,token);
    }
}
