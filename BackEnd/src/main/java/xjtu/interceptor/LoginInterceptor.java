package xjtu.interceptor;

import ch.qos.logback.core.util.StringUtil;
import io.micrometer.common.util.StringUtils;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.boot.autoconfigure.web.servlet.error.BasicErrorController;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import xjtu.annotation.Auth;
import xjtu.pojo.utils.TokenUtil;

public class LoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if(handler instanceof HandlerMethod){
            HandlerMethod handlerMethod = (HandlerMethod) handler;
            if(handlerMethod.getBean() instanceof BasicErrorController){
                return true;
            }
            Auth auth = handlerMethod.getMethod().getAnnotation(Auth.class);
            if(auth != null && auth.required()){
                String token = request.getHeader("token");
                if(StringUtils.isNotBlank(token)){
                    if(TokenUtil.verifyToken(token)) return true;
                    else{
                        request.getRequestDispatcher("/error/tokenError").forward(request,response);
                    }
                }else{
                    request.getRequestDispatcher("/error/token").forward(request,response);
                }
            }else{
                return true;
            }
        }else{
            return true;
        }
        return false;
    }
}
