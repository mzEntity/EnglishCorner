# 网上英语角PJ说明

## 运行

```
python ./Client.py
python ./Server.py
```

## 基本功能

### 登录

执行：`/login mode`

向服务器发送：

```json
{
    "header": {
        "type": "login",
        "user": ""
    },
    "body": "root"
}
{
    "header": {
        "type": "login",
        "user": ""
    },
    "body": "client"
}
```

生成userId，服务器返回：

```json
{
    "header": {
        "type": "login",
        "code": "200",
        "msg": "login success"
    },
    "body": "3ZHH21IS"
}
{
    "header": {
        "type": "login",
        "code": "400",
        "msg": "invalid mode"
    },
    "body": ""
}
```

### 管理员

假设管理员的id为root

#### /opencorner

执行：`/opencorner cornerName`

开通新的外语角，包括名字、语种等基本信息

root开通名为myCorner的，语种为English的外语角，向服务器发送：

```json
{
    "header": {
        "type": "opencorner",
        "user": "root"
    },
    "body": "myCorner\tEnglish"
}
```

服务器返回：

```json
{
    "header": {
        "type": "opencorner",
        "code": "200",
        "msg": "open corner success"
    },
    "body": ""
}

{
    "header": {
        "type": "opencorner",
        "code": "400",
        "msg": "cornerName already exists"
    },
    "body": ""
}
```

#### /corners

执行：`/corners`

列出所有开通的外语角

向服务器发送：

```json
{
    "header": {
        "type": "corners",
        "user": "root"
    },
    "body": ""
}
```

假设存在两个外语角，服务器返回：

```json
{
    "header": {
        "type": "corners",
        "code": "200",
        "msg": "list all corners"
    },
    "body": "corner1\tlanguage1\ncorner2\tlanguage2"
}
```

#### /listusers

执行：`/listusers`

列出当前所在外语角的所有用户

向服务器发送：

```json
{
    "header": {
        "type": "listusers",
        "user": "root"
    },
    "body": ""
}
```

假设存在两个用户，服务器返回：

```json
{
    "header": {
        "type": "listusers",
        "code": "200",
        "msg": "list all users"
    },
    "body": "username1\nusername2"
}
{
    "header": {
        "type": "listusers",
        "code": "400",
        "msg": "You are not in any corner."
    },
    "body": ""
}
```

#### /kickout

执行：`/kickout userId`

将某个用户踢出当前外语角，并通知当前外语角的所有其他用户

假设要踢出user1向服务器发送：

```json
{
    "header": {
        "type": "listusers",
        "user": "root"
    },
    "body": "user1"
}
```

服务器返回：

```json
{
    "header": {
        "type": "kickout",
        "code": "200",
        "msg": "kickout user successfully"
    },
    "body": "user1"
}
{
    "header": {
        "type": "kickout",
        "code": "400",
        "msg": "No such user"
    },
    "body": "user1"
}
```

#### /enter

执行`/enter cornerName`

进入某个外语角，可以看到外语角所有用户发来的信息

假设要进入myCorner，向服务器发送：

```json
{
    "header": {
        "type": "enter",
        "user": "root"
    },
    "body": "myCorner"
}
```

服务器返回：

```json
{
    "header": {
        "type": "enter",
        "code": "200",
        "msg": "enter corner successfully"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "enter",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner"
}
```

#### /exit

执行`/exit cornerName`

退出某个外语角，不再看到外语角所有用户发来的信息

假设要退出myCorner，向服务器发送：

```json
{
    "header": {
        "type": "exit",
        "user": "root"
    },
    "body": "myCorner"
}
```

服务器返回：

```json
{
    "header": {
        "type": "exit",
        "code": "200",
        "msg": "exit corner successfully"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "exit",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "exit",
        "code": "400",
        "msg": "You are not in that corner"
    },
    "body": "myCorner"
}
```

#### /closecorner

执行：`/closecorner cornerName`

关闭某个已开通的外语角，并向该外语角的所有用户发出通知

向服务器发送：

```json
{
    "header": {
        "type": "closecorner",
        "user": "root"
    },
    "body": "myCorner"
}
```

服务器返回：

```json
{
    "header": {
        "type": "closecorner",
        "code": "200",
        "msg": "close corner successfully"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "closecorner",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner"
}
```

#### /leave

退出软件

向服务器发送：

```json
{
    "header": {
        "type": "leave",
        "user": "root"
    },
    "body": ""
}
```

服务器返回：

```json
{
    "header": {
        "type": "leave",
        "code": "200",
        "msg": "goodbye"
    },
    "body": ""
}
```

### 客户

#### /corners

执行：`/corners`

列出所有开通的外语角

向服务器发送：

```json
{
    "header": {
        "type": "corners",
        "user": "user1"
    },
    "body": ""
}
```

假设存在两个外语角，服务器返回：

```json
{
    "header": {
        "type": "corners",
        "code": "200",
        "msg": "list all corners"
    },
    "body": "corner1\tlanguage1\ncorner2\tlanguage2"
}
```

#### /listusers

执行：`/listusers`

列出当前所在外语角的所有用户

向服务器发送：

```json
{
    "header": {
        "type": "listusers",
        "user": "root"
    },
    "body": ""
}
```

假设存在两个用户，服务器返回：

```json
{
    "header": {
        "type": "listusers",
        "code": "200",
        "msg": "list all users"
    },
    "body": "username1\nusername2"
}
{
    "header": {
        "type": "listusers",
        "code": "400",
        "msg": "You are not in any corner."
    },
    "body": ""
}
```

#### /join

执行：`/join cornerName userName`

以用户名username加入corner的外语角

能够随时切换到其他外语角

加入后，用户发送的信息可以被其他用户收到

假设要进入myCorner，向服务器发送：

```json
{
    "header": {
        "type": "join",
        "user": "user1"
    },
    "body": "myCorner\tanonymous"
}
```

服务器返回：

```json
{
    "header": {
        "type": "join",
        "code": "200",
        "msg": "enter corner successfully"
    },
    "body": "myCorner\tanonymous"
}
{
    "header": {
        "type": "join",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner\tanonymous"
}
{
    "header": {
        "type": "join",
        "code": "400",
        "msg": "username already exists."
    },
    "body": "myCorner\tanonymous"
}
```

#### /quit

执行`/quit cornerName`

退出某个外语角，不再看到外语角所有用户发来的信息

假设要退出myCorner，向服务器发送：

```json
{
    "header": {
        "type": "quit",
        "user": "user1"
    },
    "body": "myCorner"
}
```

服务器返回：

```json
{
    "header": {
        "type": "quit",
        "code": "200",
        "msg": "equit corner successfully"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "quit",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner"
}
{
    "header": {
        "type": "quit",
        "code": "400",
        "msg": "You are not in that corner"
    },
    "body": "myCorner"
}
```

#### /@userid

执行：`/@userid msg`

给用户id为userid的用户发送一条私人信息

向服务器发送

```json
{
    "header": {
        "type": "private",
        "user": "user1"
    },
    "body": "userid\thello world"
}
```

服务器返回：

```json
{
    "header": {
        "type": "private",
        "code": "200",
        "msg": "send message successfully"
    },
    "body": "userid\thello world"
}
{
    "header": {
        "type": "private",
        "code": "400",
        "msg": "No such user"
    },
    "body": "userid\thello world"
}
```

#### /msg

执行：`/msg cornerName msg`

在外语角corner发送一条消息

向服务器发送

```json
{
    "header": {
        "type": "msg",
        "user": "user1"
    },
    "body": "myCorner\thello everyone"
}
```

服务器返回：

```json
{
    "header": {
        "type": "msg",
        "code": "200",
        "msg": "send message successfully"
    },
    "body": "myCorner\thello everyone"
}
{
    "header": {
        "type": "msg",
        "code": "400",
        "msg": "No such corner"
    },
    "body": "myCorner\thello everyone"
}
{
    "header": {
        "type": "msg",
        "code": "400",
        "msg": "You are not in that corner"
    },
    "body": "myCorner\thello everyone"
}
```

#### /leave

退出软件

向服务器发送：

```json
{
    "header": {
        "type": "leave",
        "user": user1"
    },
    "body": ""
}
```

服务器返回：

```json
{
    "header": {
        "type": "leave",
        "code": "200",
        "msg": "goodbye"
    },
    "body": ""
}
```
