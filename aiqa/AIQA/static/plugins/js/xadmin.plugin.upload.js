var uploadWhich=-1
//**自定义上传按钮点击事件
function customUploadClick(urls){
    //检测上传文件的类型
    url = urls[uploadWhich]
    var imgName = $('#inputfile').val();
    console.log(imgName)
    var ext,idx;
    idx = imgName.lastIndexOf(".");
    if (idx != -1){
        ext = imgName.substr(idx+1).toLowerCase();
        if (ext != 'xls' && ext != 'xlsx'){
            alert("只能上传 .xls/.xlsx 类型的文件!");
        }else{
            $(function () {
                var formData = new FormData();
                var name = $("#inputfile").val();
                formData.append("file",$("#inputfile")[0].files[0]);
                formData.append("name",name);
                var csrftoken = $.getCookie('csrftoken');
                $.ajax({
                    url : url,
                    type : 'POST',
                    async : false,
                    data : formData,
                    // 告诉jQuery不要去处理发送的数据
                    processData : false,
                    // 告诉jQuery不要去设置Content-Type请求头
                    contentType : false,
                    dataType:"json",
                    beforeSend:function(xhr){
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $("#uploadAlert").modal('show');
                    },
                    success : function(responseStr) {
                        if(responseStr){
                            alert(responseStr.rst);
                        }else{
                            alert("导入失败");
                        }
                        window.location.reload();
                    }
                });
            });
        }
    } 
    else {
        alert("只能上传 .xls/.xlsx 类型的文件!");
    }
}

//**类型按钮点击事件
function selectType(action){
    uploadWhich = action
    if (action == 0){
        $("#uploadTitleLabel").html('模板');
    }else if (action == 1){
        $("#uploadTitleLabel").html('分类同义词模板');
    }
}