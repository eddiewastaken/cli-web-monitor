let event;

const eventSource = new EventSource('http://127.0.0.1:8000/monitor');
//const eventSource = new EventSource('http://10.10.10.2:8000/monitor');

eventSource.onopen = () => {
    console.log('EventSource connected')
}

eventSource.addEventListener('testEvent', function (event) {
    eventJson = JSON.parse(event.data);
    console.log('testEvent', `${JSON.stringify(eventJson)}`);
    term.write(decodeURIComponent(`${eventJson.output}`));
});

eventSource.onerror = (error) => {
    console.error('EventSource failed', error)
    eventSource.close()
}

var term = new window.Terminal({
    cursorBlink: false
});

term.open(document.getElementById('terminal'));

function init() {
    if (term._initialized) {
        return;
    }

    term._initialized = true;
}

init();
