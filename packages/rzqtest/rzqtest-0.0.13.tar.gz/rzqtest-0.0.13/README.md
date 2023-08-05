## 本包用来测试URL有效性及证书剩余时间

请用-m参数，调用

```
python -m rzqtest args...
```



参数列表说明

| 参数   | 说明                                                         |
| :----- | ------------------------------------------------------------ |
| -u     | SMTP服务的寄信人                                             |
| -k     | SMTP的授权码                                                 |
| -s     | SMTP服务器地址                                               |
| -p     | SMTP服务器端口                                               |
| -f     | 包含了URL所在的文件路径                                      |
| -l     | 收件邮箱地址列表，多个地址间以英文符号;来分隔                |
| -e     | 设置证书的剩余天数期限，默认值-1将返回所有可用的URL证书有效期限 |
| -t     | 模板文件路径，支持UTF8，默认或无法读取文件的情况下发送纯文本 |
| --func | 设置程序的工作方式，参数cert启动证书检测，参数url启动url有效性检测，默认参数all启用所有功能 |



### 自定义模版

下面是一个例子，使用模版的情况下，程序生成一组tr标签包围的数据，自定义模版应使用table标签将其嵌套。

```html
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<style type='text/css'>
		td,th{
			font-family:'微软雅黑';
			border: 2px solid #eee;
			padding: 5px 10px;
		}
		th{
			text-align: center;
		}
	</style>
</head>
<body>
	<table>
		<tr>
            <!--测试类型会匹配.title替换-->
			<th>网址</th>
			<th>.title</th>
		</tr>
        <!--测试的结果会将.content替换-->
		.content
	</table>
</body>
</html>
```

