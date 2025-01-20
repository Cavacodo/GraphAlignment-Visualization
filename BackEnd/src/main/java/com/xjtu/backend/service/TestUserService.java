package com.xjtu.backend.service;

import com.xjtu.backend.pojo.TestUser;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

/**
 * (TestUser)表服务接口
 *
 * @author makejava
 * @since 2025-01-20 14:56:53
 */
public interface TestUserService {

    /**
     * 通过ID查询单条数据
     *
     * @param  name 主键
     * @return 实例对象
     */
    TestUser queryById(String name);

    /**
     * 分页查询
     *
     * @param testUser 筛选条件
     * @param pageRequest      分页对象
     * @return 查询结果
     */
    Page<TestUser> queryByPage(TestUser testUser, PageRequest pageRequest);

    /**
     * 新增数据
     *
     * @param testUser 实例对象
     * @return 实例对象
     */
    TestUser insert(TestUser testUser);

    /**
     * 修改数据
     *
     * @param testUser 实例对象
     * @return 实例对象
     */
    TestUser update(TestUser testUser);

    /**
     * 通过主键删除数据
     *
     * @return 是否成功
     */
    boolean deleteById( );

}
