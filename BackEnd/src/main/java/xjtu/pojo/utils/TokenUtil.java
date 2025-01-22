package xjtu.pojo.utils;

import cn.hutool.core.date.DateUnit;
import cn.hutool.core.date.DateUtil;
import cn.hutool.json.JSONObject;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;

import java.util.Date;

public class TokenUtil {
    private final static String ENCRYPT_KEY = "shabishe";
    private final static int EXPIRE_TIME = 10080;
    private final static String ISSUER = "Me ";
    // 生成token
    public static String createToken(JSONObject jsonObject) {
        return JWT.create()
                .withSubject(jsonObject.toString())
                .withIssuer(ISSUER)
                .withExpiresAt(DateUtil.offsetMinute(new Date(),EXPIRE_TIME))
                .withClaim("test","123")
                .sign(Algorithm.HMAC256(ENCRYPT_KEY));
    }
    public static boolean verifyToken(String token) {
        try {
            JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(ENCRYPT_KEY)).withIssuer(ISSUER).build();
            jwtVerifier.verify(token);
            return true;
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }
}
