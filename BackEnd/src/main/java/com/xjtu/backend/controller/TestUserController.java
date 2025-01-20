package com.xjtu.backend.controller;

import com.xjtu.backend.pojo.TestUser;
import com.xjtu.backend.service.TestUserService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;

/**
 * (TestUser)表控制层
 *
 * @author makejava
 * @since 2025-01-20 14:56:53
 */
@RestController
@RequestMapping("testUser")
public class TestUserController {
    /**
     * 服务对象
     */
    @Resource
    private TestUserService testUserService;

    /**
     * 分页查询
     *
     * @param testUser 筛选条件
     * @param pageRequest      分页对象
     * @return 查询结果
     */
    @GetMapping
    public ResponseEntity<Page<TestUser>> queryByPage(TestUser testUser, PageRequest pageRequest) {
        return ResponseEntity.ok(this.testUserService.queryByPage(testUser, pageRequest));
    }

    /**
     * 通过主键查询单条数据
     *
     * @param name 主键
     * @return 单条数据
     */
    @GetMapping("{name}")
    public ResponseEntity<TestUser> queryById(@PathVariable("getName") String name) {
        return ResponseEntity.ok(this.testUserService.queryById(name));
    }

    /**
     * 新增数据
     *
     * @param testUser 实体
     * @return 新增结果
     */
    @PostMapping
    public ResponseEntity<TestUser> add(TestUser testUser) {
        return ResponseEntity.ok(this.testUserService.insert(testUser));
    }

    /**
     * 编辑数据
     *
     * @param testUser 实体
     * @return 编辑结果
     */
    @PutMapping
    public ResponseEntity<TestUser> edit(TestUser testUser) {
        return ResponseEntity.ok(this.testUserService.update(testUser));
    }

    /**
     * 删除数据
     *
     * @return 删除是否成功
     */
    @DeleteMapping
    public ResponseEntity<Boolean> deleteById() {
        return ResponseEntity.ok(this.testUserService.deleteById());
    }

}

