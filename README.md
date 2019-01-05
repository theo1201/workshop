# workshop


#Json Web Token的原理

传统方式： 采用session和cookie结合的方式
前后端分离的传统: 用户信息生成token token 和对于的用户id保存到数据库或session中。我们的drf 的 token auth 就是这种。
接着把token传给用户，存入浏览器cookie。之后的请求带上这个cookie，后端根据这个cookie值查询用户，验证过期的逻辑需要表里多一个字段，以及后端的逻辑验证。
问题: xss漏洞: cookie可以被js读取。作为后端识别用户的标识，cookie的泄露意味着用户信息不再安全。特别是drf我们的token auth没有过期时间
设置cookie时两个更安全的选项: httpOnly以及secure项.

httponly的不能被js读取，浏览器会自动加在请求header中
secure就只通过https

httponly 问题。很容易被xsrf攻击，因为cookie会默认发出去。
如果将验证信息保存数据库。每次都要查询。保存session，加大了服务器端存储压力。
只要我们生成的token遵循一定的规律，比如使用对称加密算法来加密id 形成token。
服务端只需要解密token 就能知道id。
对称加密，加密和解密使用的是同一个密钥。服务器把token传给用户，以及用户拿着token来服务器进行解密。加密解密都在服务器端。
JWT 是一个开放标准(RFC 7519)，它定义了一种用于简洁，自包含的用于通信双方之间以 JSON 对象的形式安全传递信息的方法。JWT 可以使用 HMAC 算法或者是 RSA 的公钥密钥对进行签名。它具备两个特点

简洁(Compact)可以通过URL, POST 参数或者在 HTTP header 发送，因为数据量小，传输速度快
自包含(Self-contained)负载中包含了所有用户所需要的信息，避免了多次查询数据库

JwT由三分部组成，header,payload,signature
header中包含两部分，token类型和加密算法
Payload 负载 这就是我们存放信息的地方，常用的由 iss（签发者），exp（过期时间），sub（面向的用户），aud（接收方），iat（签发时间）。
Signature 签名  前面两部分都是使用 Base64 进行编码的，即前端可以解开知道里面的信息。Signature 需要使用编码后的 header 和 payload 以及我们提供的一个密钥，
然后使用 header 中指定的签名算法（HS256）进行签名。签名的作用是保证 JWT 没有被篡改过。

1/
我们的jwt 调用的是django自带的auth与userProfile中数据进行对比。而我们如果使用手机注册，就会导致验证失败。因为默认是用用户名和密码去查的