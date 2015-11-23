
function jump(){
    window.location.href="http://news.baidu.com/";
}

var hotWords = [{name:"value1"},{name:"value2"},{name:"value3"}];
var selectedLiId ; //被选中的li的id
var num = 9;       //下拉列表里可显示的li的最大数目

searchImmediately();
document.addEventListener("keydown",function(e){onKeyDown(e);},false);

function searchImmediately(){
        var element = document.getElementById("search_input");
        if("\v"=="v") {
              element.onpropertychange = inputChange;
        }else{
              element.addEventListener("input",inputChange,false);
        } 
         
        function inputChange(){
             if(element.value){                
                 showHotWord(element.value); //建立下拉列表，函数会在下面说明
             }           
        }          
　　 }

function showHotWord(str){ //建立下拉列表
        str = $.trim(str);//去空格
        var list = window.document.getElementById("list");
        list.innerHTML = "";       
        var index = 1;
        for(var i = 0;i < hotWords.length;i++){
            var name = hotWords[i].name ;
            if(name.toLowerCase().indexOf(str.toLowerCase()) < 0) continue;
            if(index > num) break; //超过num定义的最大li数目就终止打印li
            var child = document.createElement("li");
            child.id = "word_" + index; //为每条li设置id
            
            child.onmousedown = function() {//监听鼠标按下事件                                
　　　　　　　　　 selectedLiId = null;
                getValue('search_input',this);
                showAndHide('hot_word','hide');
            }   
            child.onmouseover=function(){//监听鼠标滑上事件    
                selectedLiId = this.id;
                this.style.background="#F2F5EF"; //鼠标滑上改变li的颜色
            }
            child.onmouseout=function(){//监听鼠标滑出事件    
                this.style.background="";//鼠标滑上改回li的颜色
            }
            
             child.innerHTML = name;
             list.appendChild(child);
             index++;
         }
        
        if(index == 1) { //没搜到相关的热词，不显示下拉列表
             showAndHide('hot_word','hide'); 
             return;
        }
        var wordDiv = window.document.getElementById("hot_word");
        wordDiv.style.height = (index-1)*26+5+"px" ; //设置列表的高     
        showAndHide('hot_word','show');        
   }
   
function showAndHide(obj,types){ //下拉列表的显示与隐藏
        var Layer=window.document.getElementById(obj);
        switch(types){
            case "show":
                Layer.style.display="block";
                break;
            case "hide":
                Layer.style.display="none";
                break;
        }
   }
   
function getValue(id,obj){ //输入框获取下拉列表中被选中的li的数据 显示在输入框中
     var input=window.document.getElementById(id); 
     var li = window.document.getElementById(obj.id).innerHTML;
     input.value=li;
     search(); 
}

function onKeyDown(e){ //键盘监听器
           if (!e)  e = window.event;
           var keycode = e.which ? e.which : e.keyCode; console.log(keycode);
           switch (keycode){    
              case 13://enter键
                   var li = window.document.getElementById(selectedLiId);
                   getValue('search_input',li);
                   showAndHide('hot_word','hide');
                   break;
               case 38://上键
                   previousLi(selectedLiId);
                   break;
               case 40://下键
                   nextLi(selectedLiId);
                   break;
           }
      }
    
function nextLi(id){ //下一条li
    if(id == null) id = "word_" + num;
    var strs = id.split('_');
    var idNum = parseInt(strs[1]);  
    if(idNum == num) {
        idNum = 1;
    } else idNum++;
    selectedLiId = "word_" + idNum;
    window.document.getElementById(id).style.background="";
    window.document.getElementById(selectedLiId).style.background="#F2F5EF";
}
    
function previousLi(id){ //上一条li
    if(id == null) id = "word_" + num;
    var strs = id.split('_');
    var idNum = parseInt(strs[1]);
    if(idNum == 1) {
        idNum = num;
    } else idNum--;
    selectedLiId = "word_" + idNum;console.log(selectedLiId);
    window.document.getElementById(id).style.background="";
    window.document.getElementById(selectedLiId).style.background="#F2F5EF";
}
