function send() {
    function func1(){
        messenger.sendMessage(textArea.text)
    }

    function func2(){
        messenger.sendMessageChatGPT(textArea.text)
    }

    if (textArea.text !== '' && currentLogin == 'chatGPT_bot') {
        func2()
        textArea.text = ''
    }
    else if (textArea.text !== '' && currentLogin !== 'chatGPT_bot') {
        func1()
        textArea.text = ''
    }

}


let months = {
    0: "января",
    10: "ноября",
    11: "декабря",
    9: "октября",
    8: "сентября",
    7: "августа",
    6: "июля",
    5: "июня",
    4: "мая",
    3: "апреля",
    2: "марта",
    1: "февраля"
}

function getHandText(){
    return "nsssnnsns"
}

function getMessageTime(timestamp) {
    if (timestamp == -1) return ' '
    var date = new Date(timestamp)
    if (date.getDate() == new Date().getDate())
        return ('0' + date.getHours()).slice(-2) +
        ":"+
        ('0' + date.getMinutes()).slice(-2)
    else
        return date.getDate() +
        " " +
        months[date.getMonth()] +
        " " +
        ('0' + date.getHours()).slice(-2) +
        ":"+
        ('0' + date.getMinutes()).slice(-2)
}


function getUserTime(timestamp) {
    let date = new Date(timestamp)
    if (date.getDate() == new Date().getDate())
        return "в " + 
        ('0' + date.getHours()).slice(-2) +
        ":"+
        ('0' + date.getMinutes()).slice(-2)
    else
        return date.getDate() + 
        " " +
        months[date.getMonth()] +
        " в " +
        ('0' + date.getHours()).slice(-2) +
        ":"+
        ('0' + date.getMinutes()).slice(-2)
}

function setContacts(text) {
    if (text != '') {
        contactModel.clear()
        contactList.selectedIndex = -1
        let users = service.search(text)
        search.found = (users.length == 0) ? false : true
        for (let key in users) {
            let user = users[key]
            contactModel.append({
                contactName: [user[2], user[3]].join(' '),
                contactLogin: user[1],
                contactId: user[0],
            })
        } 
    } else {
        contactList.updateContacts()
    }
}
