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




