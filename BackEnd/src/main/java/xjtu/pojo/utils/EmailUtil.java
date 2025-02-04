package xjtu.pojo.utils;
import jakarta.mail.*;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;
import org.eclipse.angus.mail.util.MailSSLSocketFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.security.GeneralSecurityException;
import java.util.Properties;

@Component
public class EmailUtil {

    private static String host;
    private static String username;
    private static String password;

    @Value("${spring.main.host}")
    public void setHost(String host) {
        EmailUtil.host = host;
    }

    @Value("${spring.main.username}")
    public void setUsername(String username) {
        EmailUtil.username = username;
    }

    @Value("${spring.main.password}")
    public void setPassword(String password) {
        EmailUtil.password = password;
    }

    public static void sendMail(String to, String vcode) throws GeneralSecurityException {

        Properties props = System.getProperties();
        props.setProperty("mail.smtp.host", host);
        props.put("mail.smtp.auth", "true");

        //SSL加密
        MailSSLSocketFactory sf = new MailSSLSocketFactory();
        sf.setTrustAllHosts(true);
        props.put("mail.smtp.ssl.enable", "true");
        props.put("mail.smtp.ssl.socketFactory", sf);

        Session session = Session.getDefaultInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                //这个用户名密码就可以登录到邮箱服务器了,用它给别人发送邮件
                return new PasswordAuthentication(username, password);
            }
        });

        try {
            Message message = new MimeMessage(session);

            //设置发件人：
            message.setFrom(new InternetAddress(username));

            //设置收件人 这个TO就是收件人
            message.setRecipient(Message.RecipientType.TO, new InternetAddress(to));

            //邮件的主题
            message.setSubject("注册验证码");
            message.setContent("<h1>来自网站的注册用户验证码邮件,请接收你的验证码：</h1><h3>你的验证码是：" + vcode + "，请妥善保管好你的验证码！</h3>"+"<h3>5分钟内有效！</h3>", "text/html;charset=UTF-8");

            Transport.send(message);

        } catch (MessagingException mex) {
            mex.printStackTrace();
        }
    }
}
