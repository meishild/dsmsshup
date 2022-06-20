# DSM自动化 SSH更新
* 参考：http://www.up4dev.com/2017/09/11/synology-ssl-cert-update/
* 整体模式，Dokcer 运行nginx同时通过acme.sh更新ssh证书。
* 群晖宿主机通过脚本定时更新。

### 1. 下载并安装acme.sh
```
# 登入NAS
ssh -p your_port your_name@your_host
# 下载并安装acme.sh工具
curl  https://get.acme.sh | sh
```

### 2. 修改配置文件，填入你在指定域名提供商的授权token
```
# 进入到配置文件所在目录
cd ~/.acme.sh/dnsapi
# 打开阿里云的配置文件，其他提供商可以自行修改对应的配置文件
vi dns_ali.sh
# 修改如下两行配置为你自己的token，注意要去掉前面的#号
# #Ali_Key="LTqIA87hOKdjevsf5"
# #Ali_Secret="0p5EYueFNq501xnCPzKNbx6K51qPH2"
# 保存并退出vi
```

不同的提供商的token的形式和配置方式可能会有不同，需要你到域名管理的后台自己去获取。

### 3. 准备用于存放安装后的证书的目录
```
# 新建一个存放所有证书的根目录
mkdir cert_save_path
cd cert_save_path
# 为每个子域名创建对应的
mkdir sub1.example.com
mkdir sub2.example.com
# ...
```
### 4. 生成证书
```
# 首先加载acme.sh的环境变量
source ~/.acme.sh/acme.sh.env
# 执行证书获取命令，我这里的dns_ali是对应阿里云的，其他供应商可以查阅acme的文档
acme.sh --issue --dns dns_ali -d sub1.example.com
acme.sh --issue --dns dns_ali -d sub2.example.com
```

### 5. 安装证书
```
acme.sh --installcert -d sub1.example.com \
        --certpath /cert_save_path/sub1.example.com/cert.pem \
        --key-file /cert_save_path/sub1.example.com/privkey.pem \
        --fullchain-file /cert_save_path/sub1.example.com/fullchain.pem
acme.sh --installcert -d sub2.example.com \
        --certpath /cert_save_path/sub2.example.com/cert.pem \
        --key-file /cert_save_path/sub2.example.com/privkey.pem \
        --fullchain-file /cert_save_path/sub2.example.com/fullchain.pem
```

其实这里的安装是指的acme将获取的证书安装到之前建立好的目录，并没有安装到NAS自己的证书管理下边。 

### 6. 自动更新证书
* 新建计划任务，每个月运行一次
```
python /volume1/docker/nginx/ssh/update.py && /bin/nginx -s reload
```