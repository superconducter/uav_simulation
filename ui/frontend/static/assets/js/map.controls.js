L.Playback = L.Playback || {};

var loadingButton = false;

L.Playback.Control = L.Control.extend({
    _html: '',
    __html: '' +

    '<footer class="lp">' +
    '  <div class="transport">' +
    '    <div class="playback-navbar">' +
    '      <div class="playback-navbar-inner">' +
    '        <ul class="nav">' +
    '          <li class="ctrl">' +
    '            <button id="stop" class="btn btn-primary"><i id="stop-icon" class="fa fa-stop fa-lg"></i></button>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="play-pause" class="btn btn-primary"><i id="play-pause-icon" class="fa fa-play fa-lg"></i></button>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="step-backward" class="btn btn-primary"><i id="step-backward-icon" class="fa fa-step-backward fa-lg"></i></button>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="step-forward" class="btn btn-primary"><i id="step-forward-icon" class="fa fa-step-forward fa-lg"></i></button>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="clock-btn" class="clock btn btn-primary"></button>' +
    '          </li>' +
    '          <li>' +
    '            <div id="time-slider"></div>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="center-map" class="btn btn-primary"><i id="center-map-icon" class="fa fa-dot-circle-o fa-lg"></i></button>' +
    '          </li>' +
    '          <li class="ctrl dropup">' +
    '            <button id="speed-btn" style="margin-right:5px; margin-left; width:90px !important"; class="btn btn-primary" data-toggle="dropdown"><i class="fa fa-dashboard fa-lg"></i>  <span id="speed-icon-val" class="speed">1</span>x</button>' +
    '            <div class="speed-menu dropdown-menu" role="menu" aria-labelledby="speed-btn">' +
    '              <label>Playback<br/>Speed</label>' +
    '              <input id="speed-input" class="span1 speed" type="text" value="1" />' +
    '              <div id="speed-slider"></div>' +
    '            </div>' +
    '          </li>' +
    '          <li class="ctrl">' +
    '            <button id="toggle-settings" class="btn btn-primary"><i id="wrench-icon" class="fa fa-wrench fa-lg"></i></button>' +
    '          </li>' +
      '     <li class="newdata">' +
    '               <button id="loading" style="" class="btn btn-info"><i class="fa fa-refresh fa-spin"></i></button>' +

    '            <button id="newdata" style=" display: none;" class="btn btn-info btn-block" onClick="window.location.reload(true)">Click to reload new data</button>' +
    '          </li>' +
    '        </ul>' +
    '      </div>' +
    '    </div>' +
    '  </div>' +
    '</footer>' +
    ''
    ,

    initialize: function (playback) {
        this.addPlayback(playback);
    },

    addPlayback: function (playback) {
        this.playback = playback;
        if (this._getClockMode() == 'duration') {
            playback.addCallback(this._clockCallbackDuration);
        } else {
            playback.addCallback(this._clockCallback);
        }
    },

    onAdd: function (map) {
        var html = this._html;
        $('#map').after(html);
        this._setup();

        // just an empty container
        // TODO: dont do this
        return L.DomUtil.create('div');
    },

    _setup: function () {
        var self = this;
        var playback = this.playback;
        $('#play-pause').click(function () {
            if (playback.isPlaying() === false) {
                playback.start();
                $('#play-pause-icon').removeClass('fa-play');
                $('#play-pause-icon').addClass('fa-pause');
            } else {
                playback.stop();
                $('#play-pause-icon').removeClass('fa-pause');
                $('#play-pause-icon').addClass('fa-play');
            }
        });

        $('#stop').click(function () {
            
            playback.stop();
            playback.setCursor(playback.getStartTime() + 1);

            $('#play-pause-icon').removeClass('fa-pause');
            $('#play-pause-icon').addClass('fa-play');
        });

        $('#step-backward').click(function () {
            playback.setCursor(Math.max(playback.getTime() - playback.getTickLen(), playback.getStartTime()));
        });

        $('#step-forward').click(function () {
            playback.setCursor(Math.min(playback.getTime() + playback.getTickLen(), playback.getEndTime()));
        });


        var startTime = playback.getStartTime();
        this._initClock(startTime);


        $('#time-slider').slider({
            min: playback.getStartTime(),
            max: playback.getEndTime(),
            step: playback.getTickLen(),
            value: playback.getTime(),
            slide: function (event, ui) {
                playback.setCursor(ui.value);
                // alert('X');
                $('#cursor-time').val(ui.value.toString());
                // $('#cursor-time-txt').html(new Date(ui.value).toString());
            }
        });

        $('#speed-slider').slider({
            min: -9,
            max: 9,
            step: .1,
            value: self._speedToSliderVal(this.playback.getSpeed()),
            orientation: 'vertical',
            slide: function (event, ui) {
                var speed = self._sliderValToSpeed(parseFloat(ui.value));
                playback.setSpeed(speed);
                $('.speed').html(speed).val(speed);
            }
        });

        $('#speed-input').on('keyup', function (e) {
            var speed = parseFloat($('#speed-input').val());
            if (!speed) return;
            playback.setSpeed(speed);
            $('#speed-slider').slider('value', speedToSliderVal(speed));
            $('#speed-icon-val').html(speed);
            if (e.keyCode === 13) {
                $('.speed-menu').dropdown('toggle');
            }
        });


        $('.dropdown-menu').on('click', function (e) {
            e.stopPropagation();
        });

        $('#center-map').on('click', function () {
            playback._map.setView([0, 0], 2);
        });

        $('#toggle-settings').on('click', function () {
            $('#debugSettings').toggle();
        });

    },

    _getClockMode: function () {
        return 'duration'; // duration or datetime
    },


    _initClock: function (startTime) {
        if (this._getClockMode() == 'duration') {
            var _htmlClock = '              <span id="cursor-duration"></span>';

            $('.playback-navbar .clock').html(_htmlClock);

            $('#cursor-duration').html(getDuration(this.playback));

        } else if (this._getClockMode() == 'datetime') {
            var _htmlClock = '              <span id="cursor-date"></span><br/>' +
                '              <span id="cursor-time"></span>';

            $('.playback-navbar .clock').html(_htmlClock);
            $('#cursor-date').html(L.Playback.Util.DateStr(startTime));
            $('#cursor-time').html(L.Playback.Util.TimeStr(startTime));

        } else {
            throw 'Unsupported clock mode selected: ' + this._getClockMode();
        }

    },

    _clockCallback: function (ms, playback) {

        $('#cursor-date').html(L.Playback.Util.DateStr(ms));
        $('#cursor-time').html(L.Playback.Util.TimeStr(ms));

        $('#time-slider').slider('value', ms);
    },

    _clockCallbackDuration: function (ms, playback) {
        $('#cursor-duration').html(getDuration(playback));
        $('#time-slider').slider('value', ms);
    },

    _speedToSliderVal: function (speed) {
        if (speed < 1) return -10 + speed * 10;
        return speed - 1;
    },

    _sliderValToSpeed: function (val) {
        if (val < 0) return parseFloat((1 + val / 10).toFixed(2));
        return val + 1;
    },

    _combineDateAndTime: function (date, time) {
        var yr = date.getFullYear();
        var mo = date.getMonth();
        var dy = date.getDate();
        // the calendar uses hour and the timepicker uses hours...
        var hr = time.hours || time.hour;
        if (time.meridian === 'PM' && hr !== 12) hr += 12;
        var min = time.minutes || time.minute;
        var sec = time.seconds || time.second;
        return new Date(yr, mo, dy, hr, min, sec).getTime();
    }
});

var getDuration = function (playback) {
    var factor = 1 / 1000;

    if (playback && playback.getTime && playback.getStartTime && playback.getEndTime) {
        return Math.round((playback.getTime() - playback.getStartTime()) * factor) + ' / ' + (playback.getEndTime() - playback.getStartTime()) * factor;
    } else {
        return 0;
    }
};