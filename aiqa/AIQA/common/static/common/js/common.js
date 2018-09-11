/**
 *********************************************************
 ** @desc  ：工具格式化
 ** @author  Pings
 ** @date    2018-07-12
 ** @version v1.0
 * *******************************************************
 */
Date.prototype.format = function (format) {
    var o = {
        "M+": this.getMonth() + 1,    //month
        "d+": this.getDate(),         //day
        "h+": this.getHours(),        //hour
        "m+": this.getMinutes(),      //minute
        "s+": this.getSeconds(),      //second
        "q+": Math.floor((this.getMonth() + 3) / 3),   //quarter
        "S": this.getMilliseconds()   //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) 
        if (new RegExp("(" + k + ")").test(format))
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
    
    return format;
}

/**
 *********************************************************
 ** @desc  ：工具类
 ** @author  Pings
 ** @date    2018-04-23
 ** @version v1.0
 * *******************************************************
 */
class Util{

    //**get请求
    static ajax(type, url, param) {
        var csrftoken = $.getCookie('csrftoken');

        return $.ajax({
            type: type,
            url: url,
            data: param,
            //**转换成json
            dataFilter: (data, type) => JSON.parse(data),
            //**ajax头插入CSRF
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    };

    //**get请求
    static get(url) {
        return this.ajax('get', url);
    };

    //**post请求
    static post(url, param) {
        return this.ajax('post', url, param)
    };

    //**获取数据
    static getData(param, url = "/common/findall") {
        return this.post(url, param)
    };

    //**把[{name:test1,value:1},{name:test2,value:2}]转换成{{name:[test1,test2]},{value:[1,2]}}
    static toColumnsArray(dataArray) {
        let rst = new Object();

        for(let i in dataArray) {
            for(let index in dataArray[i]) {
                if(!rst[index])
                    rst[index] = new Array();
                rst[index].push(dataArray[i][index]);
            }
        }

        return rst;
    };

    //**替换dataArray中的key为toKeyObj中指定的key
    //**dataArray：[{name:test1,value:1},{name:test2,value:2}]
    //**toKeyObj：{name: name1, value: value1}
    //**结果：[{name1:test1,value1:1},{name1:test2,value1:2}]
    static replaceKey(dataArray, toKeyObj) {
        let rst = new Array();

        let jsonStr = JSON.stringify(dataArray);
        for(let i in toKeyObj) {
            let regex = new RegExp(i, "g");
            jsonStr = jsonStr.replace(regex, toKeyObj[i]);
        }

        return JSON.parse(jsonStr);
    };

    /**
     *********************************************************
     ** @desc ： 切割数组
     ** @param  dataArray  需要截取的数组：[
     **                                     {name:name1,value:value1},{name:name1,value:value2},
     **                                     {name:name2,value:value3},{name:name2,value:value4}
     **                                  ]
     ** @param  splitKey   截取的key:            name
     ** @param  srot       根据截取的key排序:     true
     ** @param  sortFun    根据截取的key排序:     排序规则
     ** @author Pings
     ** @date   2017/9/06
     ** @return rst        json：{
     **                           name1:[{name:name1,value:value1},{name:name1,value:value2}],
     **                           name2:[{name:name2,value:value3},{name:name2,value:value4}]
     **                          }
     * *******************************************************
     */
    static splitArray(dataArray, splitKey, srot = false, sortFun) {
        let splitFieldArray = splitKey ? this.toColumnsArray(dataArray)[splitKey] : dataArray;

        let set = [...new Set(splitFieldArray)];
        if(srot && sortFun) set = set.sort(sortFun);
        else if(srot) set = set.sort();

        let rst = {};
        set.forEach(field => {
            let array = new Array();
            let index = -1;
            index = splitFieldArray.findIndex((value, i) => i > index && field == value);
            while(index != -1) {
                array.push(dataArray[index]);
                index = splitFieldArray.findIndex((value, i) => i > index && field == value);
            }
            rst[field] = array;
        });

        return rst;
    };
}