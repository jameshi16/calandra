const saveEvents = async(data) => {
    const response = await fetch('http://localhost:5000/save_events',{method: 'POST', cache: 'no-cache', cors: 'no-cors', headers: {'Content-Type': 'application/json'}, redirect: 'error', body: JSON.stringify(data)});

    if (response.status === 200) {
        alert("saved successfully");
    } else {
        console.log("cannot save");
    }
}

data = [{"title": "Engineering Challenges (CSEEE-A)", "start": "2022-11-14T16:00:00", "end": "2022-11-14T18:00:00", "tag": "engf0001", "event_type": 0}, {"title": "Principles of Programming (GRP1)", "start": "2022-11-14T11:00:00", "end": "2022-11-14T13:00:00", "tag": "comp0002", "event_type": 0}]

//curl -XPOST -H "Content-type: application/json" -d '[{"title": "Engineering Challenges (CSEEE-A)", "start": "2022-11-14T16:00:00", "end": "2022-11-14T18:00:00", "tag": "engf0001", "event_type": 0}, {"title": "Principles of Programming (GRP1)", "start": "2022-11-14T11:00:00", "end": "2022-11-14T13:00:00", "tag": "comp0002", "event_type": 0}]' 'http://localhost:5000/save_events?session='
