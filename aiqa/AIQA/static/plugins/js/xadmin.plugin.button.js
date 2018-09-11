//**自定义按钮点击事件
function customButtonClick(url){
    if(!confirm("您将要执行比较消耗资源的操作，请谨慎操作！")){
        return
    }

    //**ajax提交请求
    var csrftoken = $.getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }).then(rst => alert("操作成功"), error => alert("操作失败，请稍后在试......"));
}