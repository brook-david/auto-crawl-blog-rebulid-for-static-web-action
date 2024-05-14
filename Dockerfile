# 使用官方的nginx作为基础镜像  
FROM nginx:stable-alpine  
  
# 将当前目录下的所有文件复制到nginx的web根目录  
COPY . /usr/share/nginx/html  
  
# 如果需要自定义nginx的配置，可以将配置文件放在当前目录，并复制到这里  
# 例如: COPY nginx.conf /etc/nginx/nginx.conf  
  
# 开放80端口  
EXPOSE 80  
  
# 当容器启动时，运行nginx  
CMD ["nginx", "-g", "daemon off;"]
