var echarts_left1 = echarts.init(document.getElementById('l1'), 'dark');

var echarts_left1_Option = {
    // style of title
    title: {
        text: "全国累计趋势",
        textStyle: {
            color: 'white',
        },
        left: 'left',
    },
    tooltip: {
        trigger: 'axis',
        // 指示器
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171C6'
            }
        },
    },
    legend: {
        data: ['累计确诊', '现有疑似', '累计治愈', '累计死亡'],
        left: 'right'
    },

    // 图形设置
    grid: {
        left: '4%',
        right: '6%',
        bottom: '4%',
        top: 50,
        containLabel: true
    },
    xAxis: [{
        type: 'category',
        // x轴坐标点开始与结束点位置都不在最边缘
        // boundarGap:true,
        data: []
        // data:['01.20','01.21','01.22']
    }],
    yAxis: [{
        type: 'value',
        // settings of y-axis font
        axisLabel: {
            show: true,
            color: 'white',
            fontsize: 12,
            formatter: function (value) {
                if (value >= 1000) {
                    value = value / 1000 + 'k';
                }
                return value;
            }
        },
        // settings of y-axis line
        axisLine: {
            show: true
        },
        // style of line parallel to x-axis 
        splitLine: {
            show: true,
            lineStyle: {
                color: "#17273B",
                width: 1,
                type: 'solid',
            }
        }
    }],
    series: [{
        name: '累计确诊',
        type: 'line',
        smooth: true,
        data: [],
    }, {
        name: "现有疑似",
        type: 'line',
        smooth: true,
        data: [],
    }, {
        name: "累计治愈",
        type: 'line',
        smooth: true,
        data: []
    }, {
        name: "累计死亡",
        type: 'line',
        smooth: true,
        data: []
    }]
};

echarts_left1.setOption(echarts_left1_Option)