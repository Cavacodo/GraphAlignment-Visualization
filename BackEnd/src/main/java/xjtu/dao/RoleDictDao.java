package xjtu.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

@Repository
@Mapper
public interface RoleDictDao {
    public String getRoleNameById(int role);
}
