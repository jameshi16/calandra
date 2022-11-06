BASE_URL = "https://uclapihackathon-calendar.azurewebsites.net"

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
        document.getElementById("user").innerText = json["name"];
        loadBlocks(json['events']);
    } else {
        console.log("cannot load");
    }
};

const loadBlock = (event) => {
    var title = event['title'];
    var start = event['start'];
    var end = event['end'];

    var start_date = new Date(start);
    var end_date = new Date(end);
    var startMillis = start_date.getTime();
    var endMillis = end_date.getTime();

    const duration = (endMillis - startMillis) / (1000 * 60 * 60);
    const offsetFrom0 = start_date.getHours() * 60 + start_date.getMinutes();
    const heightIntervals = document.getElementById("timeslots").offsetHeight / (24 * 4);
    const offsetFrom0Px = offsetFrom0 / heightIntervals;

    var col = 20 - start_date.getDate() + 1; // TODO: month bug (likely)
    // TODO: bug in retrieving + 7 days
    if (col > 7) col %= 7;

    var tag = document.createElement("div");
    tag.class = 'event-container';
    var row; // TODO: calculate this
    const markup = `
<div class="slot" style="position: absolute; left: ${-390 + 130 * col}px; top: ${60 * offsetFrom0Px / 4}px">
<div class="event-status" style="">
</div>
<span>${title}</span>
</div>
</div>
`;

    tag.innerHTML = markup;
    document.getElementById("event-container").appendChild(tag);
};

const loadBlocks = (eventData) => {
    // calculate the height of each block
    for (let i in eventData) {
        loadBlock(eventData[i]);
    }
};
