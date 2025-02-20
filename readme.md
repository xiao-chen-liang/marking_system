# 介绍
这是一个前后端web系统，是一个本科的毕业设计，实现了西南林业大学保研评分的自动化。
数据库使用mysql,后端使用python。
实现了docker部署，免除了配置环境的麻烦。
配置步骤如下。
有关此项目的问题可以联系 qq: 485669690. 

# 配置数据库
```shell
mysql -h hostname -u username -p postgraduate < ./postgraduate_data.sql
```

# 运行后端服务
```shell
conda env create -f environment.yml

python ./app/app.py
```

# 运行前端服务
```shell
npm install

npm run serve
```

# 使用docker-compose运行
```shell
docker-compose up
```






