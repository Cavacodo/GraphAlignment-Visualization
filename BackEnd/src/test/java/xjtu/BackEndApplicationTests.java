package xjtu;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import xjtu.pojo.utils.TokenUtil;
import xjtu.service.UserService;

@SpringBootTest
class BackEndApplicationTests {

	String token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ6bWprayIsImlzcyI6ImFkbWluIiwiZXhwIjoxNzQ3MjkwMjUwLCJyb2xlIjoidXNlciJ9.LaYmRmnR6HsgXp6Gkte27HWT0QnhXAEFRu-VFzUqXTM";

	@Autowired
	UserService  userService;
	@Test
	void testToken() {
		System.out.println(TokenUtil.parserToken(token));
	}

	@Test
	void testUserService() {
		System.out.println(userService.listAll());
	}

	@Test
	void testDelete(){
		System.out.println(userService.removeUserById(10));
	}
	@Test
	void testUpdate(){
		System.out.println();
	}
	@Test
	void contextLoads() {
	}

}
