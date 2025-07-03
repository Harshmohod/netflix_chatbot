
const { default: axios } =require("axios");
let enterpressenabled = true;
async function queryollama(prompt) {
    let fullresponse = "";
    try{
        const response =await axios.post("http://localhost;11434/api/generate",{
            model:"tinyllama",
            prompt: prompt
        });
        if(response.data) {
            const responsedata = response.data.split("\n");
            responsedata.foreach(chunk =>{
                if(chunk) {
                    const parsedchunk = JSON.parse(chunk);
                    fullresponse+= parsedchunk.response;
                }
            });
        }
    }catch(error) {
        fullresponse = "sorry,I couldn't understand that.";
    }
    return fullresponse ||"sorry, I couldn't understand that.";
}

function sendquerry() {
    const userinput= document.getElementById("userInput").valueOf;
    document.getElementById("userInput").value = "";
    togglechat(false);
    const chatbox = document.getElementById("chatbox");
    const usermessage = document.createElement("p");
    usermessage.className = "message userMessage";
    usermessage.innerHTML = `${userinput}`;
    chatbox.appendChild(usermessage);

    queryollama(userinput).then(botResponse => {
        const botMessage = document.createElement("p");
        botMessage.className = "message botmessage";
        botMessage.innerHTML = "";
        chatbox.appendChild(botMessage);
        typewriterEffect(botMessage,botResponse,() => togglechat(true));
        document.getElementById("userinput").value = "";
    }).catch(error => {
        const botmessage = document.createElement("p");
        botmessage.className = "message botmessage";
        botmessage.innerHTML = "sorry, I couldn't understand that.";
        chatbox.appendChild(botmessage);
    })
}

function togglechat(enable) {
    submitbutton.disabled = !enable;
    submitbutton.classlist.toggle("disabled",!enable);
    enterpressenabled = enable;
}

function typewriterEffect(element,text, callback) {
    let i=0;
    function type() {
        if(i<text.length) {
            element.innerHTML +=text.charat(i);
            i++;
            setTimeout(type,20);
            scrollToBottom();
        }else if (callback){
            callback();
        }
    }
    type();
}

function scrollToBottom() {
    const chatcontainer = document.getElementById("chatbox=container");
    chatcontainer,scrolltop = chatcontainer.scrollHeight;
}

document.getElementById("userinput").addEventListener("keypress",function(event){
    if(event.key = "Enter" && enterpressenabled) {
        event.preventDefault();
        sendquerry();
        scrollToBottom();
    }
});