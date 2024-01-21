const currentDate = new Date();
function getYear(date){
    const year = currentDate.getFullYear().toString(); // 년도를 그대로 가져옵니다.

    return year;
}
function getMonth(flag){
    //flag == 1 "01"형식으로
    //flag == 0 "1" 형식으로
    month = (currentDate.getMonth() + 1).toString().padStart(2, '0'); // 월은 0부터 시작하므로 +1 필요
    monStr = month.toString();
    if(flag == 0){
        month = monStr.startsWith("0")?monStr.replace("0",""):month;
    }
    return month
}
function getDay(flag){
    //flag == 1 "01"형식으로
    //flag == 0 "1" 형식으로
    day = currentDate.getDate().toString().padStart(2, '0');
    dayStr = day.toString();
    if(flag == 0){
        day = dayStr.startsWith("0")?dayStr.replace("0",""):day;
    }
    return day
}
function getHours(){
    const hours = currentDate.getHours().toString().padStart(2, '0');
    return hours
}
function getMinutes(){
    const minutes = currentDate.getMinutes().toString().padStart(2, '0');
    return minutes
}

