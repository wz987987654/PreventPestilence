$(function () {
    $("#switch").on("click",function () {
        if ($("#switch").val() == "邮箱登陆"){
            document.getElementById("emaildiv").style.display = "block";
            document.getElementById("teldiv").style.display = "none";
                $("#switch").val("手机登陆");
        } else {
            $("#switch").val("邮箱登陆");
            document.getElementById("emaildiv").style.display = "none";
            document.getElementById("teldiv").style.display = "block";
        }
    })
})