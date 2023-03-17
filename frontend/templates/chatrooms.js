function listChatroomsOnPage(data) {
    const ul = document.getElementById('chatroom')

    for (let key in data) {
        const li = document.createElement('li');

        var content = '';
        content += data[key]['name'];

        li.appendChild(document.createTextNode(content));
        ul.appendChild(li);
    }
}

function loadChatrooms() {
    fetch('http://127.0.0.1:8000/api/chatrooms')
    .then(response => response.json())
    .then(data => listChatroomsOnPage(data))
}

loadChatrooms();