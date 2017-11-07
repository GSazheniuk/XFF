function distance(aX, aY, bX, bY){
    return +(Math.sqrt(Math.pow(bX - aX, 2) + Math.pow(bY - aY, 2))).toFixed(2);
}

enums = {
    UfoStatuses: ['Appearing', 'Moving', 'Leaving', 'Engaging', 'Fleeing', 'Crashed']
}