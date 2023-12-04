# 网上英语角PJ说明



## 基本功能



### 服务器端

#### /opencorner

开通新的外语角，包括名字、语种等基本信息

```json
{
    "header": {
        "mode": "command",
        "type": "opencorner",
        "cornerName": "*",
        "language": "*"
    },
    "body": ""
}
```

### 客户端

#### /corners

列出所有开通的外语角

```json
{
    "header": {
        "mode": "command",
        "type": "corners"
    },
    "body": ""
}
```

#### /listusers

列出当前所在外语角的所有用户

```json
{
    "header": {
        "mode": "command",
        "type": "listusers"
    },
    "body": ""
}
```

