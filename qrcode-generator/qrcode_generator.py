import qrcode

def qrcode_wifi(wifi_name, wifi_password, output_png):
    text = 'WIFI:S:{};T:WPA;P:{};;'.format(wifi_name, wifi_password)
    img = qrcode.make(text)
    img.save(output_png)

def qrcode_simple_text(text, output_png):
    img = qrcode.make(text)
    img.save(output_png)


def qrcode_email(email, subject, message,output_png):
    text = 'MATMSG:TO:{};SUB:{};BODY:{};;'.format(email, subject,message)
    img = qrcode.make(text)
    img.save(output_png)

def qrcode_phone_number(tel, output_png):
    text = 'tel:{}'.format(tel)
    img = qrcode.make(text)
    img.save(output_png)

qrcode_wifi('test','test', 'example_qrcode.png')
qrcode_simple_text('http://www.google.com/', 'out.png')
qrcode_email(email='test@test.com', subject='test', message='test', 'out.png')
qrcode_phone_number(tel='123456789', 'out.png')


