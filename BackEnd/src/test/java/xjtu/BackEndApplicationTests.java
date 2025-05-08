package xjtu;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import xjtu.pojo.utils.TokenUtil;

@SpringBootTest
class BackEndApplicationTests {

	String token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ6bWprayIsImlzcyI6ImFkbWluIiwiZXhwIjoxNzQ3MjkwMjUwLCJyb2xlIjoidXNlciJ9.LaYmRmnR6HsgXp6Gkte27HWT0QnhXAEFRu-VFzUqXTM";
	@Test
	void testToken() {
		System.out.println(TokenUtil.parserToken(token));
	}

	@Test
	void contextLoads() {
	}

}
