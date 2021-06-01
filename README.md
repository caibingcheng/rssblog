# RSSBlog 0.2

![RSSBlog](./static/screenshot.png)

RSSBlog 是一个基于RSS的博客内容聚合站. 想法来源: [https://github.com/volfclub/travellings](https://github.com/volfclub/travellings) 及 [https://front-end-rss.vercel.app/](https://front-end-rss.vercel.app/)

通过RSSBlog将方便地预览不同博客的标题, 而无需进入不同的博客浏览. RSSBlog使用时间戳排序, 越新的文章将排列在越前.

## 接入规则

### 加入RSSBlog的博客应满足

1. 愿为开放的网络做出贡献(如乐于分享知识经验等)
2. 没有违法以及影响体验的内容(如侵入式广告等)
3. 正常更新维护中(国内无法正常访问会被移除)
4. 网页已有较多内容
5. 启用https

### 提交issue

如果满足RSSBlog的接入条件, 且期望接入RSSBlog, 需要按照以下格式提交issue:
```
{
    link: 'https://yourblog.com/rss.xml',
    author: 'yourname'
}
```
提交的issue将经过人工筛选, 以保证内容干净.

### RSS接力

目前还没有非常确定的定义RSSBlog的接力规则, 所以目前可以您的博客网站中无需有指向RSSBlog的链接, 当然有的话最好了.

您可以在底部或者其他地方接入:
```HTML
<a href="http://rssblog.vercel.app/" target="_blank" rel="noopener" title="RSSBlog">
    <i class='fas fa-fw fa-inbox'></i>RSSBlog
</a>
```
```fa-inbox```看起来像一个盒子, 比较贴近RSS聚合的定义.

有任何问题或者建议欢迎提issue.

## 参与贡献

本站目前欢迎任何形式的贡献, 您可以:
1. 更改样式;
2. 页面设计;
3. 重构代码;
4. 任何其他;

在项目后期, 或者项目版本迭代到1.0之后将会控制重构及该版等较大的改动.

### TODOLIST

目前还有一些TODO的功能:
1. 分类: 时间分类[年, 年月, 等], 内容分类[技术, 杂谈, 生活, 等]
2. 搜索: 标题搜索和内容搜索

## 任何问题

欢迎提issue, 我们会尽量阅读并回复.