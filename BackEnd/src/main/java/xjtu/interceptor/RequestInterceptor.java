package xjtu.interceptor;

import io.jsonwebtoken.Claims;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.commons.lang3.StringUtils;
import org.springframework.web.servlet.HandlerInterceptor;
import xjtu.pojo.utils.TokenUtil;

public class RequestInterceptor implements HandlerInterceptor {
    private final TokenUtil tokenUtil;
    public RequestInterceptor(TokenUtil tokenUtil) {
        this.tokenUtil = tokenUtil;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 获取请求头
        String header = request.getHeader("Authorization");

        // 请求头不为空进行解析
        if (StringUtils.isNotBlank(header)) {
            // 按照我们和前端约定的格式进行处理
            if (header.startsWith("Bearer ")) {
                // 得到令牌
                String token = header.substring(7);

                // 验证令牌
                try {
                    // 令牌的解析这里一定的try起来,因为它解析错误的令牌时,会报错
                    Claims claims = tokenUtil.parserToken(token);
                    String roles = (String) claims.get("role");
                    String url = request.getRequestURI();

                    if (roles != null && "admin".equals(roles)) {
                        request.setAttribute("admin", token);
                    }
                    if (roles != null && "user".equals(roles)) {
                        request.setAttribute("user", token);
                    }
                    if(url.startsWith("/all")){
                        if(roles.equals("admin")){
                            request.setAttribute("admin", token);
                            return true;
                        }else{
                            response.setStatus(403);
                            return false;
                        }
                    }
                    return true;
                } catch (Exception e) {
                    throw new RuntimeException("令牌不存在");
                }
            }
            response.setStatus(403);
            return false;
        }
        response.setStatus(403);
        return false;
    }
}
