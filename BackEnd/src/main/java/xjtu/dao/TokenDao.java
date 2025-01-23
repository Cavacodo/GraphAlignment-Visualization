package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import xjtu.pojo.User;

@Mapper
@Repository
public interface TokenDao {
    public String getTokenByAccount(String account);
    public int setToken(String account, String token);
    public int deleteToken(String account);
    public int addToken(String account, String token);
}
