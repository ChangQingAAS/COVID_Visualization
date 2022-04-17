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