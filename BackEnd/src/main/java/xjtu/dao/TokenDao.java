package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface TokenDao {
    public String getTokenByAccount(String account);
    public int setToken(String account, String token);
    public int deleteToken(String account);
}
