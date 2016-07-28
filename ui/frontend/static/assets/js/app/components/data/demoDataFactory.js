/**
 * Created by nkuehl on 04/07/16.
 * This Factory provides demo data for use in the map and other places
 */

(function () {
    'use strict';

    angular.module('app.factory.demoData', [])
        .factory('demoData', [
            function () {
                return {
                    trackA1: function () {
                        return {
                            "title": "a1",
                            "groupIds": ["a", "moving"],
                            "color": "blue",
                            "visualType": "friendly_uav",
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPoint",
                                "coordinates": [
                                    [0, 1],
                                    [0, 10],
                                    [0, 11]
                                ]
                            },
                            "properties": {
                                "changes": [
                                    {status: "primary"},
                                    {status: "success"},
                                    {status: "warning"}
                                ],
                                "time": [
                                    1000,
                                    2000,
                                    3000
                                ]
                            }
                        };
                    },
                    trackA2: function () {
                        return {
                            "title": "a2",
                            "groupIds": ["a", "moving"],
                            "color": "blue",
                            "visualType": "flag",
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPoint",
                                "coordinates": [
                                    [10, 10],
                                    [5, 10],
                                    [6, 10]


                                ]
                            },
                            "properties": {
                                "changes": [
                                    {status: "warning"},
                                    {},
                                    {status: "danger"}
                                ],
                                "time": [

                                    3000,
                                    4000,
                                    5000
                                ]
                            }
                        };
                    },

                    trackB: function () {
                        return {
                            "title": "b1",
                            "groupIds": ["b", "moving"],
                            "color": "darkred",
                            "visualType": "hostile_uav",
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPoint",
                                "coordinates": [
                                    [10, 2],
                                    [1, 5],
                                    [2, 6],
                                    [100, 6]

                                ]
                            },
                            "properties": {
                                "changes": [
                                    {status: "ok"},
                                    {},
                                    {status: "danger"},
                                    {status: "ok"}
                                ],
                                "time": [
                                    1000,
                                    2000,
                                    3000,
                                    4000
                                ]
                            }
                        };
                    },

                    emptyTrack: function () {
                        return {
                            "title": "",
                            "groupIds": [],
                            "color": "darkred",
                            "visualType": "hostile_uav",
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPoint",
                                "coordinates": []
                            },
                            "properties": {
                                "changes": [],
                                "time": []
                            }
                        };
                    },

                    staticA: function () {

                        return {
                            type: 'polygon',
                            points: [[5, 15],
                                [5, 25],
                                [15, 20]],
                            groupIds: ['group-a', 'group-static']
                        };
                    },

                    staticB: function () {
                        return {
                            type: 'polygon',
                            points: [
                                [1, 10],
                                [2, 12],
                                [15, 30],
                                [10, 30]
                            ],
                            groupIds: ['group-b', 'group-static']
                        };
                    },

                    events: function () {
                        return {

                            "2000": [
                                {type: "package_delay", location: [15, 10]}
                            ],
                            "3000": [
                                {type: "package_pickup", location: [6, 10]}
                            ],
                            "4000": [
                                {type: "package_lost", location: [16, 10]},
                                {type: "package_delivered"}
                            ]
                        };
                    },

                    almostEmptyTrack: function () {
                        return {
                            "title": "",
                            "groupIds": [],
                            "color": "darkred",
                            "visualType": "hostile_uav",
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPoint",
                                "coordinates": [[1, 2],]
                            },
                            "properties": {
                                "changes": [],
                                "time": [100]
                            }
                        };
                    },

                    trackData: function () {
                        return {
                            objectTypes: {
                                drone: {
                                    type: "circle",
                                    radius: 300000,
                                    options: {
                                        fillColor: "#0fff0f",
                                        fillOpacity: 0.7,
                                        color: "#000000",
                                        weight: 5
                                    },
                                    status: {
                                        "primary": {},
                                        "warning": {
                                            fillColor: "#00ffff",
                                            weight: 10
                                        },
                                        "danger": {
                                            fillColor: "#ff0000",
                                            weight: 20
                                        },
                                        "success": {
                                            fillColor: "#00ff00",
                                            weight: 5
                                        }
                                    }
                                },
                                hostile_uav: {
                                    type: "rectangle",
                                    length: 10,
                                    options: {
                                        fillColor: "#ff0000"
                                    },
                                    status: {
                                        "primary": {},
                                        "warning": {
                                            fillColor: "#00ffff",
                                            weight: 10
                                        },
                                        "danger": {
                                            fillColor: "#ff0000",
                                            weight: 20
                                        },
                                        "success": {
                                            fillColor: "#00ff00",
                                            weight: 5
                                        }
                                    }
                                },
                                /*flag: {
                                 type: "awesome",
                                 options: {
                                 prefix: 'fa',
                                 icon: 'flag',
                                 markerColor: 'purple'
                                 }
                                 }*/
                            },
                            eventTypes: []/*{
                             package_lost: {
                             name: "Package Lost",
                             description: "A package that was supposed to be delivered got lost.",
                             class: "alert alert-danger",
                             markerOptions: {
                             fillColor: '#ff0000'
                             }
                             },
                             package_pickup: {
                             name: "Package Pickup",
                             description: "A package was picked up by a UAV.",
                             class: "alert alert-success"
                             },
                             package_delay: {
                             name: "Package Delay",
                             description: "A package is delayed.",
                             class: "alert alert-warning"
                             },
                             package_delivered: {
                             name: "Package Delivered",
                             description: "A package was successfully delivered.",
                             class: "alert alert-success"
                             }
                             },*/,

                            moving: [this.almostEmptyTrack()],
                            static: [],//[staticA, staticB],
                            events: [],//events,
                            groups: []/*[
                             {
                             name: "Group A", id: "a", subgroups: [
                             {name: "A - Moving", id: "moving", subgroups: []},
                             {name: "A - Static", id: "static", subgroups: []}
                             ]
                             },
                             {name: "Group B", id: "b", subgroups: []}
                             ]*/
                        };
                    },

                    x: function () {
                        return {
                            "name": "Yet another simulation",
                            "description": "Tell some details about the simulation...",
                            "objectTypes": {},
                            "eventTypes": {
                                package_lost: {
                                    name: "Package Lost",
                                    description: "A package that was supposed to be delivered got lost.",
                                    class: "alert alert-danger"
                                },
                                package_pickup: {
                                    name: "Package Pickup",
                                    description: "A package was picked up by a UAV.",
                                    class: "alert alert-success"
                                },
                                package_delay: {
                                    name: "Package Delay",
                                    description: "A package is delayed.",
                                    class: "alert alert-warning"
                                },
                                package_delivered: {
                                    name: "Package Delivered",
                                    description: "A package was successfully delivered.",
                                    class: "alert alert-success"
                                }
                            }
                        };
                    }
                }
            }])
})();