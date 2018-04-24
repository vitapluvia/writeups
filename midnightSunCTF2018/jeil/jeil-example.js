var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);

var Jail = (function() {
    var rv = {};

    function secretFuncUnguessable11011000110111101101100(a,b,c){
        if(a === 'foo' && b === 'bar' && c === 'baz'){
            return true;
        }
    }

    function call(code) {
        var line = "";

        if(new RegExp(/[\[\]\.\\\+\-\/;a-zA-Z{}`'"\s]/).test(code)){
            console.log("Unrecognized code.");
            throw 123;
            return;
        }

        if(!(code.length == 32)){
            console.log("Incorrect code length.");
            throw 123;
            return;
        }

        arguments = undefined;

        ret = null;
        ret = eval("this.secretFuncUnguessable"+code);

        if(typeof ret == "function"){
            if(ret.call(this,'foo', 'bar', 'baz') === true){
                console.log("FLAG{F4k3_Fl4g!!!}");
            }else{
                console.log("Incorrect code.");
            }
        }else{
            console.log("Incorrect code.");
        }
        throw 123;
    };
    rv.call = call;
    rv.toString = function(){return rv.call.toString()};

    return rv;
})();

template = `|￣￣￣￣￣￣￣￣|  
|    Internal    |
|＿＿＿＿＿＿＿＿|
       ||
(\\__/) || 
(•ㅅ•) || 
/ 　 づ  

Code: `;

function ask(){
    rl.question(template,function(answer){
        Jail.call(answer);
    });
}

ask();



