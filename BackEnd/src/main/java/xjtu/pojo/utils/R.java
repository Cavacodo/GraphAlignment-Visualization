package xjtu.pojo.utils;

import lombok.Data;

import java.io.Serial;
import java.io.Serializable;

// 统一的响应类
@Data
public class R<T> implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private Integer code;
    private String msg;
    private T data;
    private R(){

    }
    public static <T> R<T> ok(T data){
        R<T> response = new R<>();
        response.setCode(ResponseEnum.SUCCESS.getCode());
        response.setMsg(ResponseEnum.SUCCESS.getMsg());
        response.setData(data);
        return response;
    }
    public static <T> R<T> error(ResponseEnum responseEnum){
        R<T> response = new R<>();
        response.setCode(responseEnum.getCode());
        response.setMsg(responseEnum.getMsg());
        return response;
    }
    public static <T> R<T> error(Integer errorCode,String errorMsg){
        R<T> response = new R<>();
        response.setCode(errorCode);
        response.setMsg(errorMsg);
        return response;
    }
}
