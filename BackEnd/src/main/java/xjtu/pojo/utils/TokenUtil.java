package xjtu.pojo.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwt;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.util.Date;

public class TokenUtil {
    private final static byte[] ENCRYPT_KEY = "e_key".getBytes(StandardCharsets.UTF_8);;
    private final static int EXPIRE_TIME = 60 * 24;
    private final static String ISSUER = "admin";
    // 生成token
    public static String createToken(String username, String role) {
        return Jwts.builder()
                .setSubject(username)
                .setIssuer(ISSUER)
                .setExpiration(Date.from(Instant.now().plus(Duration.ofMinutes(EXPIRE_TIME))))
                .claim("role", role)
                .signWith(SignatureAlgorithm.HS256, ENCRYPT_KEY)
                .compact();
    }
    public static Claims parserToken(String token) {
        return Jwts.parser()
                .setSigningKey(ENCRYPT_KEY)
                .parseClaimsJws(token)
                .getBody();
    }
}
