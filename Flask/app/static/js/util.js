/**
 * Created by limeng on 2017/10/30.
 */

function CaseInfoSave() {
      var CaseName = $("#Casename").val();
      var CaseDes = $("#CaseDes").val();
      var projects = $("#projects").val();
      //console.log(CaseName);

      $.post(
              '/SaveCaseInfo',
              {
                  "Casename": CaseName,
                  "CaseDes": CaseDes,
                  "projects": projects
              },
              function (data, status) {
                  if (data) {
                      //console.log(data.toString())//data是为用例Id
                      alert(data);
                      $("#caseid").val(data.toString())

                  } else {
                      alert("保存失败");
                  }
              });
};


//case 增加接口时,子页面增加数据,父页面显示的函数

function  ParentCaseInterShow(){
    var CaseName = $("#Casename").val();
    $.post(
              '/getShowCaseByName',
              {
                  "Casename": CaseName,

              },
              function (data, status) {
                  if (data) {
                      var str="";
                      var data=eval("("+data+")");
                     for(var i=0;i<data.length;i++){
                        str += "<tr>" +
                                "<td>" + data[i].interface_name+ "</td>" +
                                "<td>" + data[i].interface_url+ "</td>" +
                        "</tr>";
                     };
                      alert(str);
                      $("#tbody-result").html(str);
                     // window.location.reload();
                  } else {
                      alert("保存失败");
                  }
              });




}


//创建用例方法

function createCase(){
    var CaseName = $("#Casename").val();
     $.post(
              '/createCase',
              {
                  "Casename": CaseName
              },
              function (data, status) {
                  if (data) {
                      alert("用例创建成功");
                  } else {
                      alert("创建失败");
                  }
              });

}










