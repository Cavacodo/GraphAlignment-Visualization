package com.xjtu.backend.dao;

import com.xjtu.backend.pojo.TestUser;
import org.springframework.data.domain.Pageable;
import java.util.List;

/**
 * (TestUser)表数据库访问层
 *
 * @author makejava
 * @since 2025-01-20 14:56:53
 */
public interface TestUserDao {

    /**
     * 通过ID查询单条数据
     * @return 实例对象
     */
    TestUser queryById(String name);


    long count(TestUser testUser);

    /**
     * 新增数据
     *
     * @param testUser 实例对象
     * @return 影响行数
     */
    int insert(TestUser testUser);


    int update(TestUser testUser);

    /**
     * 通过主键删除数据
     *
     * @return 影响行数
     */
    int deleteById( );

}

