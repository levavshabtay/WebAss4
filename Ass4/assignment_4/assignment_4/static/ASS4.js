function myFunction() {
    fetch('https://reqres.in/api/users').then(
        response => response.json()
    ).then(
        response => createUsersList(response.data)
    ).catch(
        err => console.log(err)
    )
}

function createUsersList(users) {
    const id = document.getElementById("user_id").value;
    const curr_main = document.querySelector("main");
    let index = 0;
    for (let user of users) {
        index += 1;
        const section = document.createElement('section');
        if (id == index) {
            section.innerHTML = `<img src="${user.avatar}" alt="Profile Picture"/><br>    
                                     <h4>full name : ${user.first_name} ${user.last_name}</h4>
                                     <h4>email : ${user.email}</h4><br>`;
            curr_main.appendChild(section);
        }
    }
}
