function distance(aX, aY, bX, bY){
    return +(Math.sqrt(Math.pow(bX - aX, 2) + Math.pow(bY - aY, 2))).toFixed(2);
}

function listen2queue(endpoint, callback){
        var xhr = new XMLHttpRequest();
        xhr.open("GET", endpoint, true);
        xhr.onprogress = callback;
        xhr.send();
}

enums = {
    UfoStatuses: ['Appearing', 'Moving', 'Leaving', 'Engaging', 'Fleeing', 'Crashed'],
    SkillStatuses: {
        Available: 0,
        Unavailable: 1,
        InProgress: 2,
        Queued: 3,
    }
}