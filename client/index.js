BASE_URL = "http://localhost:5000"

const saveEvents = async(data) => {
    const response = await fetch(BASE_URL + '/save_events',{method: 'POST', cache: 'no-cache', cors: 'no-cors', headers: {'Content-Type': 'application/json'}, redirect: 'error', body: JSON.stringify(data)});

    if (response.status === 200) {
        alert("saved successfully");
    } else {
        console.log("cannot save");
    }
}

const onLoginClick = () => {
    window.location.href = BASE_URL + '/login';
}

function getQueryVariable(variable)
{
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return(false);
}

const loadEvents = async () => {
    var session = getQueryVariable("session");
    if (!session) {
        console.log("no session found");
        location.href = "/index.html";
        return;
    }

    const response = await fetch(BASE_URL + '/consolidated_timetable?session=' + session, {method: 'GET', cache: 'no-cache', cors: 'no-cors', headers: {'Content-Type': 'application/json'}, redirect: 'error'});

    if (response.status === 200) {
        const json = await response.json();
        console.log(json);
    } else {
        console.log("cannot load");
    }
}
