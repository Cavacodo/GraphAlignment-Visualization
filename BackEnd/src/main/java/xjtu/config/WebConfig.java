package xjtu.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import xjtu.interceptor.CrossInterceptorHandler;
import xjtu.interceptor.RequestInterceptor;
import xjtu.pojo.utils.TokenUtil;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new CrossInterceptorHandler()).addPathPatterns("/**");
        registry.addInterceptor(new RequestInterceptor(new TokenUtil())).addPathPatterns("/**")
                .excludePathPatterns("/user/login/**")
                .excludePathPatterns("/user/register/**")
                .excludePathPatterns("/user/forgetPassword/**")
                .excludePathPatterns("/res/python");
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:5173")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowCredentials(true)
                .allowedHeaders("*")
                .maxAge(3600);
    }
}