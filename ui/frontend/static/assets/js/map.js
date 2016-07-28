/**
 * Overwrite LeafletSim theme settings (see L.Sim.Theme for details)
 * 
 */

L.Sim.Theme.defaultIconUrl = '/static/assets/images/drone.png';

L.Sim.Theme.displayObjectDetails = function (icon) {
    
    // Add icon to detail view
    if (icon._icon) {
        var iconClone = $(icon._icon).clone(); //cloneNode(true).childNodes[0];
        $(iconClone).css({
            margin: '0px auto',
            position: 'relative',
            top: '0px',
            left: '0px',
            transform: 'none'
        });
        $('#objectDetailsPanel .panel-body').html(iconClone); //.outerHTML);
    } else {
        // $('#objectDetailsPanel .panel-body').html('N/A');
    }

    // Add data to scope
    var scope = angular.element($("#objectDetailsPanel")).scope();
    scope.$apply(function () {

        var location = (icon._latlng && icon._latlng.lat && icon._latlng.lng) ? icon._latlng.lng + ' / ' + icon._latlng.lat : ' (invalid position)';

        scope.selectedPin = {
            leafletId: icon._leaflet_id,
            data: icon._data,
            loc: location,
            properties: icon.agentProperties
        };
    });
    $('#objectDetailsPanelMsg').hide();
    $('#objectDetailsPanel').show();
};

L.Sim.Theme.addEventToLog = function (typeInfo, location) {
    var fadeOutDuration = 3000;
    var logContainer = $('#events');

    var div = document.createElement('div');

    // Build DOM according to event type config
    // var eventType = event.getTypeInfo();

    if (typeInfo) {
        var str = '<strong>' + typeInfo.title + ':</strong> ' + typeInfo.description;
        if (location)
            str += ' (@ ' + location + ')';

        $(div).html(str);
        $(div).addClass(typeInfo.class);
    } else {
        $(div).text('Unknown Event');
        $(div).addClass('alert alert-info');
    }

    logContainer.append(div);

    $(div).fadeOut(fadeOutDuration);
};