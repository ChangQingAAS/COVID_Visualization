function showTime() {
    var date = new Date()
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var day = date.getDate()
    var hour = date.getHours()
    var minute = date.getMinutes()
    var second = date.getSeconds()
    if (hour < 10) {
        hour = "0" + hour
    }
    if (minute < 10) {
        minute = "0" + minute
    }
    if (second < 10) {
        second = "0" + second
    }
    var time = year + "年" + month + "月" + day + "日" + hour + ":" + minute + ":" + second
    $("#tim").html(time)
}

setInterval(showTime, 1000) //1秒调用1次


function get_c1_data() {
    $.ajax({
        url: "/c1",
        success: function (data) {
            //分别选中各个元素并填充内容
            console.log(data);
            $(".num h1").eq(0).text(data.confirm);
            $(".num h1").eq(1).text(data.suspect);
            $(".num h1").eq(2).text(data.heal);
            $(".num h1").eq(3).text(data.dead);
        },
        error: console.error('请求c1数据失败')
    });
}

function get_c2_data() {
    $.ajax({
        url: "/c2",
        success: function (data) {
            echarts_center_option.series[0].data = data.data
            echarts_center.setOption(echarts_center_option)
        },
        error: console.error('请求c2数据失败')
    });
}

function get_l1_data() {
    echarts_left1.showLoading()
    $.ajax({
        url: "/l1",
        success: function (data) {
            echarts_left1_Option.xAxis[0].data = data.day
            echarts_left1_Option.series[0].data = data.confirm
            echarts_left1_Option.series[1].data = data.suspect
            echarts_left1_Option.series[2].data = data.heal
            echarts_left1_Option.series[3].data = data.dead
            echarts_left1.setOption(echarts_left1_Option)
            echarts_left1.hideLoading()
        },
        error: console.error('请求l1数据失败')
    });
}

function get_l2_data() {
    $.ajax({
        url: "/l2",
        success: function (data) {
            var update_time = data.update_time
            var details = data.details
            var risk = data.risk
            $("#l2 .ts").html("截至时间：" + update_time)
            var s = ""
            for (var i in details) {
                if (risk[i] == "高风险") {
                    s += "<li><span class='high_risk'>高风险\t\t</span>" + details[i] + "</li>"
                } else {
                    s += "<li><span class='middle_risk'>中风险\t\t</span>" + details[i] + "</li>"
                }
            }
            $("#risk_wrapper_li1 ul").html(s)
            start_roll()
        },
        error: function (xhr, type, errorThrown) {}
    })
}

function get_r1_data() {
    $.ajax({
        url: "/r1",
        success: function (data) {
            echarts_right1_option.xAxis.data = data.city;
            echarts_right1_option.series[0].data = data.confirm;
            echarts_right1.setOption(echarts_right1_option);
        },
        error: console.error('请求r1数据失败')
    })
}

function get_r2_data() {
    $.ajax({
        url: "/r2",
        success: function (data) {
            echarts_right2_option.series[0].data = data.kws;
            echarts_right2.setOption(echarts_right2_option);
        }
    })
}

function refreshPage() {
    window.location.reload()
}

get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()

// setInterval(gettime, 1000)
// setInterval(get_c1_data, 1000 * 10)
// setInterval(get_c2_data, 10000 * 10)
// setInterval(get_l1_data, 10000 * 10)
// setInterval(get_l2_data, 10000 * 10)
// setInterval(get_r1_data, 10000 * 10)
// setInterval(get_r2_data, 1000 * 10)