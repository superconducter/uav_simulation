// Array.prototype.implode does not work!?
var richArrayImplode = function (arr, delimiter, prefix, suffix) {
    var delimiter = delimiter || ', ';
    var prefix = prefix || '';
    var suffix = suffix || '';

    var s = '';
    for (var i = 0; i < arr.length; i++) {
        if (s.length == 0) {
            s = prefix + arr[i] + suffix;
        } else {
            s += delimiter + prefix + arr[i] + suffix;
        }
    }
    return s;
};

function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
}

function randomWithSeed(seed) {
    var x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
}

Array.prototype.randomChoiceKey = function (seed) {
    var seed = seed || 1;
    var rand = randomWithSeed(seed);
    rand *= this.length;
    rand = Math.floor(rand);

    return rand;
};


var setTitle = function (title) {
    var title = title || '';

    if (title.length > 0) {
        $('#title').html('&nbsp; / ' + title);
    } else {
        $('#title').html('');
    }
};