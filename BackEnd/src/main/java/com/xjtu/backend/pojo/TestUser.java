package com.xjtu.backend.pojo;
import lombok.Data;


public class TestUser {
    private String name;
    private int password;

    public String getName() {
        return this.name;
    }
}
