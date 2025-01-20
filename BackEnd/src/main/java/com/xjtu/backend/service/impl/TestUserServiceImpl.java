package com.xjtu.backend.service.impl;

import com.xjtu.backend.pojo.TestUser;
import com.xjtu.backend.dao.TestUserDao;
import com.xjtu.backend.service.TestUserService;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import javax.annotation.Resource;

/**
 * (TestUser)表服务实现类
 *
 * @author makejava
 * @since 2025-01-20 14:56:53
 */
@Service("testUserService")
public class TestUserServiceImpl implements TestUserService {
    @Resource
    private TestUserDao testUserDao;

    /**
     * 通过ID查询单条数据
     *
     * @return 实例对象
     */
    @Override
    public TestUser queryById(String name) {
        return this.testUserDao.queryById(name);
    }

    @Override
    public Page<TestUser> queryByPage(TestUser testUser, PageRequest pageRequest) {
        return null;
    }

    /**
     * 分页查询
     *
     * @param testUser 筛选条件
     * @param pageRequest      分页对象
     * @return 查询结果
     */

    /**
     * 新增数据
     *
     * @param testUser 实例对象
     * @return 实例对象
     */
    @Override
    public TestUser insert(TestUser testUser) {
        this.testUserDao.insert(testUser);
        return testUser;
    }

    /**
     * 修改数据
     *
     * @param testUser 实例对象
     * @return 实例对象
     */
    @Override
    public TestUser update(TestUser testUser) {
        this.testUserDao.update(testUser);
        return this.queryById(testUser.getName());
    }

    /**
     * 通过主键删除数据
     *
     * @return 是否成功
     */
    @Override
    public boolean deleteById( ) {
        return this.testUserDao.deleteById() > 0;
    }
}
