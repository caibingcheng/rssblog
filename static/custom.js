var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?4d63ba711285f7c696d0505f5e30ba96";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();

// 通知栏关闭功能
function closeNotice() {
  var noticeBar = document.getElementById('notice-bar');
  if (noticeBar) {
    noticeBar.classList.add('hidden');
  }
}

// 30秒后自动关闭通知栏
window.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    closeNotice();
  }, 30000); // 30秒 = 30000毫秒
});
