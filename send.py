import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

def start_auto_smtp_client():
    print("=====================================================")
    print("       推免申请邮件 - 动态称呼自动发送工具")
    print("=====================================================\n")
    
    # 北交大 SMTP 服务器配置 (指南明确：SMTP端口465，使用SSL)
    mail_server = 'mail.bjtu.edu.cn' 
    port = 465
    
    # 请在此处配置您的北交邮箱
    sender_email = 'your_id@bjtu.edu.cn'
    print(f"当前发件人邮箱: {sender_email} (请在脚本中修改)")
    
    # 密码建议通过输入获取，不要硬编码在代码中
    password = input("请输入该邮箱的SMTP登录密码: ").strip()
    
    # 邮件主题模板
    subject_template = "202x级推免生 申请 - [您的姓名] - 北京交通大学"

    # 无限循环轮询
    while True:
        print("\n" + "-"*50)
        receiver_email = input(">>> 1. 请输入【收件人邮箱】 (输入 q 退出): ").strip()
        if receiver_email.lower() == 'q':
            break
        
        receiver_name = input(">>> 2. 请输入【老师姓名】 (例如: 董老师): ").strip()
        if not receiver_email or not receiver_name:
            print("[!] 邮箱和姓名不能为空，请重新输入。")
            continue

        # 动态构造正文内容（请根据您的实际情况修改以下模板）
        body = f"""尊敬的{receiver_name}老师：

您好！我叫***，是北京交通大学***专业***级的本科生。我十分渴望能在 202x 年秋季加入您的课题组深造。

我们在专业内排名 ***/***，前五学期加权平均成绩 ***，预计将取得推免资格。在本科期间，我打下了数学与代码基础，还投入了大量的精力在***领域的科研实践中，并取得了一些实质性成果。

随信附上我的个人简历、成绩单以及相关证明材料。不知您今年是否还有招生名额？如果有机会，希望能与您进行一次简短的线上交流，或者完成您课题组的考核任务。

感谢您在百忙之中阅读我的邮件。祝您工作顺利，身体健康！

***
电话： ***********
邮箱： {sender_email}
就读院校： 北京交通大学 ***学院"""

        # 自动获取附件列表（排除当前脚本本身）
        current_script = os.path.basename(sys.argv[0])
        attachments = [f for f in os.listdir('.') if os.path.isfile(f) and f != current_script]
        
        print(f"[*] 准备发送至: {receiver_name} 老师 ({receiver_email})")
        print(f"[*] 附件列表: {', '.join(attachments) if attachments else '无'}")

        # ---------------------------------------------------------
        # 1. 构建安全的 MIME 邮件对象
        # ---------------------------------------------------------
        msg = MIMEMultipart()
        # 规范化发件人格式，防止被识别为垃圾邮件
        msg['From'] = formataddr((Header("您的姓名", 'utf-8').encode(), sender_email))
        msg['To'] = receiver_email
        msg['Subject'] = Header(subject_template, 'utf-8')

        # 挂载正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 挂载附件（标准库会自动处理 Base64 和文件头拆分）
        for filename in attachments:
            try:
                with open(filename, "rb") as f:
                    part = MIMEApplication(f.read(), Name=filename)
                # 使用 Header 编码文件名，防止中文附件名乱码
                part.add_header('Content-Disposition', 'attachment', filename=Header(filename, 'utf-8').encode())
                msg.attach(part)
            except Exception as e:
                print(f"[X] 读取附件 {filename} 失败: {e}")
                continue

        # ---------------------------------------------------------
        # 2. 连接服务器并发送
        # ---------------------------------------------------------
        try:
            print("\n[*] 正在连接到SMTP服务器(SSL 465端口)...")
            server = smtplib.SMTP_SSL(mail_server, port)
            
            print("[*] 正在进行身份认证...")
            server.login(sender_email, password)
            print("[✓] 认证成功！")
            
            print("[*] 正在发送邮件内容及附件...")
            server.sendmail(sender_email, [receiver_email], msg.as_string())
            print(f"[√] 发送成功！已投递至 {receiver_name} 老师的邮箱。")
            
            server.quit()

        except smtplib.SMTPAuthenticationError:
            print("[X] 登录失败: 密码错误。请检查输入的是否是正确的邮箱登录密码或授权码。")
        except Exception as e:
            print(f"[X] 发生错误: {e}")

    print("\n程序正常退出。祝你投递顺利！")

if __name__ == '__main__':
    start_auto_smtp_client()
