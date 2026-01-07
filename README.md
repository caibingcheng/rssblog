## RSSBlog

<img width="1763" height="934" alt="image" src="https://github.com/user-attachments/assets/4e77dcc6-500a-4666-afa5-02a42e09da1f" />

RSSBlog 是一个基于RSS的博客内容聚合站. 想法来源: [volfclub/travellings](https://github.com/volfclub/travellings) 及 [front-end-rss](https://front-end-rss.vercel.app/)

### 接入规则

#### 加入条件

1. 愿为开放的网络做出贡献(如乐于分享知识经验等)
2. 没有违法以及影响体验的内容(如侵入式广告等)
3. 正常更新维护中(国内无法正常访问会被移除)
4. 网页已有较多内容
5. 启用https

#### 提交

一般情况下，贴上你的订阅链接即可，通过提交[issue](https://github.com/caibingcheng/rssblog/issues)：
```
"https://imcbc.cn/index.xml"
```

提交的[issue](https://github.com/caibingcheng/rssblog/issues)将经过人工筛选, 以保证内容干净.

#### RSS接力

您可以在底部或者其他地方接入:
```HTML
<a href="https://rssblog.imcbc.cn" target="_blank" rel="noopener" title="RSSBlog">
    <i class='fas fa-fw fa-inbox'></i>RSSBlog
</a>
```
```fa-inbox```看起来像一个盒子, 比较贴近RSS聚合的定义.
