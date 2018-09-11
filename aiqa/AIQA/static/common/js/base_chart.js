/**
 *********************************************************
 ** @desc  ： 基础chart类
 ** @author  Pings
 ** @date    2017-09-11
 ** @version v1.0
 * *******************************************************
 */
var BaseEChart = class BaseEChart {

    constructor(id, params) {
        this._id_ = id;
        this._myChart_ = echarts.init($("#" + this._id_).get(0));
        this._params_ = params;
        this._option_;
        this._series_;
        this._baseData_;
        this._isSetData_ = false;
        //**是否显示图例
        this._isShowLegend_ = true;
    }

    //**获取原始数据，只能在echarts事件里面使用
    getBaseData() {
        return this._baseData_;
    }

    //**获取echart对象
    getEChart() {
        return this._myChart_;
    }

    //**设置参数
    setOption(option) {
        this._option_ = option;
    }

    //**设置查询参数
    setParams(params) {
        if(this._params_ && params) {
            $.extend(true, this._params_, params);
        }
    }

    //**设置是否显示图例
    setIsShowLegend(flag) {
        this._isShowLegend_ = flag;
    }

    //**启用方法,返回Deferred对象，包含原始数据
    show() {
        let self = this;

        return this.getData().then(function(dataArray){
            self.parseData(dataArray);
            self._myChart_.setOption(self.getOption(), true);
        }).then(function(){
            let def = $.Deferred();
            def.resolve(self._baseData_);
            return def.promise();
        });
    }

    //**获取数据
    getData() {
        if(this._isSetData_ && this._baseData_) {
            let def = $.Deferred();
            def.resolve(this._baseData_);
            return def.promise();
        } else
            return Util.getData(this._params_);
    }

    //**设置数据
    setData(data) {
        this._isSetData_ = true;
        this._baseData_ = data;
    }

    //**解析数据
    parseData(dataArray) {
        this._baseData_ = dataArray;
    }

    //**获取echart option
    getOption() {}
}

/**
 *********************************************************
 ** @desc  ： 柱状图
 ** @author  Pings
 ** @date    2017-09-14
 ** @version v1.0
 * *******************************************************
 */
var BaseBar = class BaseBar extends BaseEChart {

    constructor(id, params, legendFiled = "baseBarLegend") {
        super(id, params);

        this._legendFiled_ = legendFiled;
        this._axisData_;

        if(this._isShowLegend_)
            this._legendData_ = [legendFiled];

        //**Y轴显示
        this._isY_ = false;
    }

    //**设置Y轴显示
    setIsY(flag) {
        this._isY_ = flag;
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        this._series_ = [{name: this._legendFiled_, type: 'bar', data: dataArray.map(obj => obj.value)}];
        this._axisData_ = dataArray.map(obj => obj.name);
    }

    //**获取echart option
    getOption() {
        //**_isY_=false y轴显示值,_isY_=true,x轴显示值
        let category = {
            type : 'category',
            data : this._axisData_
        };
        let value = {
            type : 'value'
        };
        let xAxis = this._isY_ ? value : category;
        let yAxis = this._isY_ ? category : value;

        let option = {
            tooltip : {
                trigger: 'axis',
                axisPointer : {
                    type : 'shadow'
                }
            },
            legend: {
                data: this._legendData_,
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: xAxis,
            yAxis: yAxis,
            series: this._series_
        };

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}

/**
 *********************************************************
 ** @desc  ： 三维柱状图
 ** @author  Pings
 ** @date    2017-09-11
 ** @version v1.0
 * *******************************************************
 */
var PileBar = class PileBar extends BaseBar {

    constructor(id, params, legendFiled, seriesStack = "pileBarStack") {
        super(id, params, legendFiled);

        this._seriesStack_ = seriesStack;
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        let dataJson = Utils.splitArray(dataArray, this._legendFiled_);
        let index = 0;
        this._legendData_ = new Array();
        this._series_ = new Array();

        for(let key in dataJson) {
            if(!(index++))
                this._axisData_ = dataJson[key].map(obj => obj.name);

            if(this._isShowLegend_)
                this._legendData_.push(key);

            this._series_.push({
                name: key,
                type: 'bar',
                stack: this._seriesStack_,
                data: dataJson[key]
            });
        }
    }
}

/**
 *********************************************************
 ** @desc  ： 饼图
 ** @author  Pings
 ** @date    2017-09-15
 ** @version v1.0
 * *******************************************************
 */
var BasePie = class BasePie extends BaseEChart {

    constructor(id, params, seriesName = "basePieSeries") {
        super(id, params);

        this._seriesName_ = seriesName;
        this._legendData_;

        //**是否是空心圆
        this._isHollow_ = false;
        //**是否是南丁格尔图
        this._isAngle_ = false;
    }

    //**是否是空心圆
    setIsHollow(flag) {this._isHollow_ = flag;}

    //**是否是南丁格尔图
    setIsAngle(flag) {this._isAngle_ = flag;}

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        if(this._isShowLegend_)
            this._legendData_ = dataArray;

        this._series_ = [{name: this._seriesName_, type:'pie', data: dataArray, radius: '60%'}];
    }

    //**获取echart option
    getOption() {
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                data: this._legendData_
            },

            series: this._series_
        };

        if(this._isHollow_)
            option.series[0].radius = ['40%', '55%'];
        if(this._isAngle_)
            option.series[0].roseType =  'angle';

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}

/**
 *********************************************************
 ** @desc  ： 三维饼图
 ** @author  Pings
 ** @date    2017-09-15
 ** @version v1.0
 * *******************************************************
 */
var PilePie = class PilePie extends BasePie {

    //**解析数据
    parseData(firstDataArray, secondDataArray) {
        super.parseData({first: firstDataArray, second: secondDataArray});

        if(this._isShowLegend_)
            this._legendData_ = firstDataArray;

        this._series_ = [
            {
                name: this._seriesName_,
                type: 'pie',
                radius: [0, '30%'],
                label: {
                    normal: {
                        position: 'inner'
                    }
                },
                data: firstDataArray
            },
            {
                name: this._seriesName_,
                type: 'pie',
                radius: ['40%', '60%'],
                data: secondDataArray
            }
        ];
    }

    //**获取数据
    getData() {
        return $.when(Utils.getData(this._params_.first), Utils.getData(this._params_.second));
    }

    //**启用方法
    show() {
        let self = this;

        return this.getData().then(function(firstDataArray, secondDataArray){
            self.parseData(firstDataArray[0], secondDataArray[0]);
            self._myChart_.setOption(self.getOption(), true);
        }).then(function(){
            let def = $.Deferred();
            def.resolve(self._baseData_);
            return def.promise();
        });
    }
}

/**
 *********************************************************
 ** @desc  ： 基础雷达图
 ** @author  Pings
 ** @date    2017-09-18
 ** @version v1.0
 * *******************************************************
 */
var BaseRadar = class BaseRadar extends BaseEChart {

    constructor(id, params, legendFiled = "baseRadarLegend") {
        super(id, params);

        this._legendFiled_ = legendFiled;

        if(this._isShowLegend_)
            this._legendData_ = [legendFiled];

        this._seriesName_ = legendFiled;
        this._radarIndicator_;
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        this._radarIndicator_ = dataArray;
        this._series_ = [{
            name: this._legendData_,
            type: 'radar',
            data: [{
                value: dataArray.map(json => json.value),
                name: this._legendData_
            }]
        }];
    }

    //**获取echart option
    getOption() {
        var option = {
            tooltip: {
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: this._legendData_,
                textStyle:{
                    color:"#CCC"
                }
            },
            radar: {
                indicator: this._radarIndicator_,
                name: {
                    textStyle: {
                        color: '#eee'
                    }
                }
            },
            series: this._series_
        };

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}

/**
 *********************************************************
 ** @desc  ： 三维雷达图
 ** @author  Pings
 ** @date    2017-09-18
 ** @version v1.0
 * *******************************************************
 */
var PileRadar = class PileRadar extends BaseRadar {

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        let dataJson = Utils.splitArray(dataArray, this._legendFiled_);
        let index = 0;
        this._legendData_ = new Array();
        this._series_ = [{
            name: this._legendFiled_,
            type: 'radar',
            data: []
        }];

        for(let key in dataJson) {
            if(!(index++))
                this._radarIndicator_ = dataJson[key];

            if(this._isShowLegend_)
                this._legendData_.push(key);

            this._series_[0].data.push({name: key, value: dataJson[key].map(json => json.value)});
        }
    }
}

/**
 *********************************************************
 ** @desc  ：漏斗图
 ** @author  Pings
 ** @date    2017-09-27
 ** @version v1.0
 * *******************************************************
 */
var BaseFunnel = class BaseFunnel extends BaseEChart {

    constructor(id, params, seriesName = "baseFunnelSeries") {
        super(id, params);

        this._seriesName_ = seriesName;
        this._legendData_;
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        if(this._isShowLegend_)
            this._legendData_ = dataArray;

        this._series_ = [{}];
        this._series_[0].data = dataArray;
    }

    //**获取echart option
    getOption() {
        let option = {
            tooltip: {
                trigger: 'item'
            },
            legend: {
                data: this._legendData_,
                textStyle: {
                    color: "#ccc"
                }
            },
            // backgroundColor: "#001a32",
            calculable: true,
            series: [{
                name: this._seriesName_,
                type: 'funnel',
                left: '10%',
                top: 60,
                bottom: 60,
                width: '80%',
                sort: 'descending',
                gap: 0,
                label: {
                    normal: {
                        show: true,
                        position: 'inside',
                        textStyle:{
                            color:'#efefef'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        length: 40,
                        length2:10,
                        lineStyle: {
                            width: 1,
                            type: 'solid',
                        }
                    }
                },
                itemStyle: {
                    normal: {
                        // borderColor: '#fff',
                        borderWidth: 0
                    }
                },
                data: this._series_[0].data,
            }]
        };

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}

/**
 *********************************************************
 ** @desc  ：拆线图
 ** @author  Pings
 ** @date    2017-09-27
 ** @version v1.0
 * *******************************************************
 */
var BaseLine = class BaseLine extends BaseEChart {

    constructor(id, params, legendFiled = "baseLineLegend") {
        super(id, params);

        this._legendFiled_ = legendFiled;
        this._xAxisData_;

        if(this._isShowLegend_)
            this._legendData_ = [legendFiled];
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        this._xAxisData_ = dataArray.map(obj => obj.name);

        this._series_ = [{}];
        this._series_[0].data = dataArray;
    }

    //**获取echart option
    getOption() {
        var option = {
            color: ['#0066cc'],
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                data: this._xAxisData_,
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        color: "#488ec3",
                        width: 2
                    }
                },
                axisLabel: {
                    color: "#CCC"
                }

            }],
            yAxis: [{
                type: 'value',
                axisLine: {
                    lineStyle: {
                        color: "#488ec3",
                        width: 2
                    }
                },
                splitLine: {
                    lineStyle: {
                        type: "dotted",
                    }
                },
                axisLabel: {
                    color: "#CCC"
                }
            }],
            series: [{
                name: this._legendFiled_,
                type: 'line',
                barWidth: '60%',
                symbol: "emptyCircle",
                lineStyle: {
                    normal: {
                        color: "#96cc3e",
                    }
                },
                data: this._series_[0].data
            }]
        };

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}

/**
 *********************************************************
 ** @desc  ： 三维拆线图
 ** @author  Pings
 ** @date    2017-09-27
 ** @version v1.0
 * *******************************************************
 */
var PileLine = class PileLine extends BaseLine {

    constructor(id, params, legendFiled, seriesStack = "pileLineStack") {
        super(id, params, legendFiled);

        this._seriesStack_ = seriesStack;
    }

    //**解析数据
    parseData(dataArray) {
        super.parseData(dataArray);

        let dataJson = Utils.splitArray(dataArray, this._legendFiled_);
        let index = 0;
        this._legendData_ = new Array();
        this._series_ = new Array();

        for(let key in dataJson) {
            if(!(index++))
                this._xAxisData_ = dataJson[key].map(obj => obj.name);

            if(this._isShowLegend_)
                this._legendData_.push(key);

            this._series_.push({
                name: key,
                type: 'line',
                stack: this._seriesStack_,
                showSymbol: false,
                data: dataJson[key]
            });
        }
    }

    //**获取echart option
    getOption() {
        let option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: this._legendData_
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: this._xAxisData_
            },
            yAxis: {
                type: 'value'
            },
            series: this._series_
        };

        if(this._option_) {
            $.extend(true, option, this._option_);
        }

        return option;
    }
}
