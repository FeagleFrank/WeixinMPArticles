# WeixinMPArticles

使用python抓取某公众号所有历史文章

## 使用方法：
使用WireShark或者Fiddler进行抓包，需要获取两个地址：
公众号历史文章redirect前的地址```url```，Like this：
>https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=xxx==&uin=xxx&key=xxx&devicetype=xxx&version=xxx&lang=zh_CN&ascene=x&pass_ticket=xxx

公众号历史文章页翻页Ajax请求地址```url_link```，Like this：
>https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=xxx==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=xxx&pass_ticket=xxx&wxtoken=&appmsg_token=xxx&x5=0&f=json

填入```url```与```url_link```中运行即可
