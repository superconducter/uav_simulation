/**
 * Wrapper for the LeafletSim plugin
 * - adds data to LeafletSim
 * - sets map settings
 * - handles static agents
 */

(function () {
    'use strict';

    angular.module('app.factory.mapWrapper', ['app.factory.settingsParser', 'app.factory.demoData'])
        .factory('mapWrapperFactory', [
            function () {
                var MapWrapper = function (containerId, data) { // Constructor
                    this.containerId = containerId || 'map';
                    this.data = data || {};
                    this.debug = true;
                };

                MapWrapper.prototype.init = function () { // Call this to add map to container
                    this.map = new L.Map(this.containerId, {
                        crs: L.CRS.Simple,
                        minZoom: this.data.minZoom || 0,
                        maxZoom: this.data.maxZoom || 8,
                        zoomControl: true,
                        center: this.data.center || [30.0, 3.0], // Center map and default zoom level
                        zoom: this.data.zoom || 2
                    });

                    this.setBackground();
                    this.setStaticAgents(this.data.static);

                    // Playback options
                    var enableClusters = (this.data.hasOwnProperty('clusters') && this.data.clusters == false ? false : true);
                    console.log(this.data.hasOwnProperty('clusters'));
                    var playbackOptions = {
                        // layer and marker options
                        layer: {
                            pointToLayer: this.drawTracks // Add colored GPS track to map
                        },
                        events: this.data.events,
                        eventTypes: this.data.eventTypes,
                        objectTypes: this.data.objectTypes,
                        enableClusters: enableClusters
                    };

                    if (this.debug) {
                        console.log('ObjectTypes: ', this.data.objectTypes);
                        console.log('EventTypes: ', this.data.eventTypes);
                        console.log('Agents (moving) data: ', this.data.moving);
                        console.log('Agents (static) data: ', this.data.static);
                        console.log('Event data: ', this.data.events);
                        console.log('Enable clusters: ', playbackOptions.enableClusters);
                    }


                    // Initialize playback or L.Sim if available
                    if (L.Sim) {
                        this.playback = new L.Sim(this.map, this.data.moving, null, playbackOptions);
                    } else {
                        this.playback = new L.Playback(this.map, this.data.moving, null, playbackOptions);
                    }

                    // Initialize custom control
                    this.control = new L.Playback.Control(this.playback);
                    this.control.addTo(this.map);

                };

                MapWrapper.prototype.drawTracks = function (featureData, latlng) { // Add colored GPS track to map
                    var result = {};

                    if (featureData && featureData.properties && featureData.properties.path_options) {
                        result = featureData.properties.path_options;
                    }

                    if (!result.radius) {
                        result.radius = 5; // Default radius
                    }

                    // Get random color depending on type
                    var colors = [
                        {color: '#1A5D73', fillColor: '#90C3D4'},
                        {color: '#361A73', fillColor: '#7B56CC'},
                        {color: '#83069C', fillColor: '#B856CC'},
                        {color: '#9C0656', fillColor: '#F073B6'},
                        {color: '#BA0000', fillColor: '#FF4040'},
                        {color: '#00912E', fillColor: '#40FF7C'},
                        {color: '#78C93A', fillColor: '#3F9100'},
                        {color: '#98B300', fillColor: '#E5FF54'},
                        {color: '#B35F00', fillColor: '#FF8800'}
                    ];
                    var randColorKey = colors.randomChoiceKey(hashCode(featureData.visualType));
                    if (colors[randColorKey]) {
                        result.color = colors[randColorKey].color;
                        result.fillColor = colors[randColorKey].fillColor;
                    }

                    return new L.CircleMarker(latlng, result);
                };

                MapWrapper.prototype.setData = function (data) {
                    // this.playback.addData(data);
                    this.data = data;
                };

                MapWrapper.prototype.setBackground = function () {

                    // Adds the background layer to the map
                    if (this.data.backgroundImage && this.data.backgroundPosition) {
                        // L.imageOverlay('/static/assets/images/map_background.png', [[0, 0], [100, 100]]).addTo(this.map);
                        L.imageOverlay(this.data.backgroundImage, this.data.backgroundPosition).addTo(this.map);

                    }


                    // Use grid instead of background image
                    if ((this.data.hasOwnProperty('grid') && !this.data.grid ? false : true)) {
                        var options = {
                            interval: 20,
                            showOriginLabel: true,
                            redraw: 'moveend',
                            zoomIntervals: [
                                {start: 0, end: 3, interval: 50},
                                {start: 4, end: 5, interval: 5},
                                {start: 6, end: 20, interval: 1}
                            ]
                        };
                        L.simpleGraticule(options).addTo(this.map);
                    }

                };

                MapWrapper.prototype.setStaticAgents = function (agents) {
                    var layerObjects = [];

                    for (var i in agents) {
                        var agent = agents[i];
                        var typeInfo = L.Sim.getTypeInfo(this.data, agent.visualType);

                        if (!agent.title)
                            continue;

                        // console.log('STATIC = ', agent);

                        if (agent.geometry && agent.geometry.coordinates && agent.geometry.coordinates.length > 0) { // At least one location is required

                            var pos = agent.geometry.coordinates[0]; // Only use first location
                            var icon;
                            typeInfo.options.clickable = true;

                            // Define icon depending on type
                            if (typeInfo.type == 'awesome') {
                                var icon = L.marker(pos);
                                icon.setIcon(L.Sim.icon(typeInfo.options, typeInfo));

                            } else if (typeInfo.type == 'rectangle') {
                                var h = typeInfo.options.width || 10,
                                    w = typeInfo.options.height || 10;

                                var points = typeInfo.options.points || [
                                        pos,
                                        [pos[0] + w, pos[1]],
                                        [pos[0] + w, pos[1] + h],
                                        [pos[0], pos[1] + h]
                                    ];
                                // console.log('DRAW STATIC: ', agent);
                                icon = L.polygon(points, typeInfo.options);

                            } else if (typeInfo.type == 'circle') {
                                var radius = typeInfo.options.radius || 1;
                                radius *= 78000; // Leaflet radius is strange

                                // console.log('Circle pos: ', pos, ' r = ', radius);
                                icon = L.circle(pos, radius, typeInfo.options);
                            } else {
                                console.error('Unsupported object type: ', typeInfo.type);
                                continue;
                            }

                            // Draw
                            // icon._latlng = pos;
                            icon._data = {
                                type: typeInfo.name,
                                title: agent.title,
                                groupIds: agent.groupIds
                            };
                            icon.agentProperties = agent.properties.changes[0] || {};
                            icon.agentProperties.static = true;
                            icon.on('click', function (context) {
                                console.log('>>', context);
                                console.log('__ this', this);
                                L.Sim.displayObjectDetails(this);

                            });
                            icon.addTo(this.map);

                        }

                    }
                };

                return MapWrapper;
            }])
})();
