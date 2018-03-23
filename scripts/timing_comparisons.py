import os
CGE_USERNAME = os.getenv('CGE_USERNAME')
CGE_PASSWORD = os.getenv('CGE_PASSWORD')

# CGE uses session tokens

# ------WebKitFormBoundary8qpBIQO8d9P63CBo
# Content-Disposition: form-data; name="configfile"
#
# /srv/www/htdocs/services/CGEpipeline-1.1/config.cf
# ------WebKitFormBoundary8qpBIQO8d9P63CBo
# Content-Disposition: form-data; name="userID"
#
# kle
# ------WebKitFormBoundary8qpBIQO8d9P63CBo
# Content-Disposition: form-data; name="usersession"
#
# 0b510a7aa5d04855274e8813aee3ee368c748580
# ------WebKitFormBoundary8qpBIQO8d9P63CBo
# Content-Disposition: form-data; name="userip"
#
# 76.64.201.22
# ------WebKitFormBoundary8qpBIQO8d9P63CBo
# Content-Disposition: form-data; name="uploadpath"
#
# /home/data2/secure-upload/isolates/6_23_3_2018_1212_270_450188/
# ------WebKitFormBoundary8qpBIQO8d9P63CBo--

# curl 'https://cge.cbs.dtu.dk/cgi-bin/webface.fcgi' -H 'Pragma: no-cache' -H 'Origin: https://cge.cbs.dtu.dk' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,la;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundary8qpBIQO8d9P63CBo' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Referer: https://cge.cbs.dtu.dk/services/cge/' -H 'Cookie: PHPSESSID=pg6nvnj7egldig8bl2584qbi5ueaijf6rkrja4kmeo75g1isk8n0' -H 'Connection: keep-alive' -H 'DNT: 1' --data-binary $'------WebKitFormBoundary8qpBIQO8d9P63CBo\r\nContent-Disposition: form-data; name="configfile"\r\n\r\n/srv/www/htdocs/services/CGEpipeline-1.1/config.cf\r\n------WebKitFormBoundary8qpBIQO8d9P63CBo\r\nContent-Disposition: form-data; name="userID"\r\n\r\nkle\r\n------WebKitFormBoundary8qpBIQO8d9P63CBo\r\nContent-Disposition: form-data; name="usersession"\r\n\r\n0b510a7aa5d04855274e8813aee3ee368c748580\r\n------WebKitFormBoundary8qpBIQO8d9P63CBo\r\nContent-Disposition: form-data; name="userip"\r\n\r\n76.64.201.22\r\n------WebKitFormBoundary8qpBIQO8d9P63CBo\r\nContent-Disposition: form-data; name="uploadpath"\r\n\r\n/home/data2/secure-upload/isolates/6_23_3_2018_1212_270_450188/\r\n------WebKitFormBoundary8qpBIQO8d9P63CBo--\r\n' --compressed

# curl 'https://cge.cbs.dtu.dk/cgi-bin/webface.fcgi?jobid=5AB527C800006415D6BA7C51;wait=' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,la;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: no-cache' -H 'Referer: https://cge.cbs.dtu.dk/services/cge/' -H 'Cookie: PHPSESSID=pg6nvnj7egldig8bl2584qbi5ueaijf6rkrja4kmeo75g1isk8n0' -H 'Connection: keep-alive' --compressed

# Date: Fri, 23 Mar 2018 16:14:01 GMT
