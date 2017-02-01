/* eslint no-console: 0 */
'use strict';

import React, { Component } from 'react';
import {
    AppRegistry,
    StyleSheet,
    Text,
    TextInput,
    View,
    DeviceEventEmitter  //react-native-sensor-manager
} from 'react-native';


// Sensor manager
// var sensorManager = require("NativeModules").SensorManager;
import { SensorManager } from 'NativeModules';


export default class masApp extends Component {
    constructor(props) {
        super(props);
        watchID: (null: ?number);  //FIXME: is this necesary?
        this.state = {
            lat: 0,
            lon: 0,
            speed: 0,
            accuracy: 0,
            altitude: 0,
            altitudeAccuracy: 0,
            heading: 0,

            x: 0,
            y: 0,
            z: 0,

            xg: 0,
            yg: 0,
            zg: 0,

            azimuth: 0, // Yaw
            pitch: 0,
            roll: 0,

            steps: 0,

            activity: "Unknown"
        };
    }

    componentDidMount() {
        this.watchID = navigator.geolocation.watchPosition((position) => {
                var lon = position.coords.longitude;
                var lat = position.coords.latitude;
                var speed = position.coords.speed;
                var accuracy = position.coords.accuracy;
                var altitude = position.coords.altitude;
                // var altitudeAccuracy = position.coords.altitudeAccuracy;
                var heading = position.coords.heading;


                this.setState({
                    lat: lat,
                    lon: lon,
                    speed: speed,
                    accuracy: accuracy,
                    altitude: altitude,
                    // altitudeAccuracy: altitudeAccuracy,
                    heading: heading
                });
                this.fetchGeolocation(lat,lon,speed,accuracy,altitude,heading,this.state.activity);
                // TODO: test geolocation her, hindre geolocation i å rendre eller sensorene

            },
            (error) => alert(JSON.stringify(error)),
            {enableHighAccuracy: false, timeout: 20000, maximumAge: 0, setInterval: 300}
            //FIXME: setintervall?
        );

        SensorManager.startAccelerometer(300); // Start the accelerometer with a minimum delay of 100 ms between events
        DeviceEventEmitter.addListener("Accelerometer", function (data) {
            var x = data.x;
            var y = data.y;
            var z = data.z;

            this.setState({
                x: x,
                y: y,
                z: z
            });
        }.bind(this));

/*
        SensorManager.startGyroscope(300);
        DeviceEventEmitter.addListener("Gyroscope", function (data) {
            var xg = data.x;
            var yg = data.y;
            var zg = data.z;

            this.setState({
                xg: xg,
                yg: yg,
                zg: zg
            });
        }.bind(this));

        SensorManager.startOrientation(300);
        DeviceEventEmitter.addListener('Orientation', function (data) {
            var azimuth = data.azimuth; // Yaw
            var pitch = data.pitch;
            var roll = data.roll;

            this.setState({
                azimuth: azimuth, // Yaw
                pitch: pitch,
                roll: roll
            });

        }.bind(this));

        SensorManager.startStepCounter(300);
        DeviceEventEmitter.addListener('StepCounter', function (data) {
            var steps = data.steps;

            this.setState({
                steps: steps
            });
        }.bind(this));*/
    }



    fetchGeolocation(lat, lon, speed, accuracy, altitude, heading, activity) {


        var URL = "http://188.166.168.99:5000/storeGNSS?lat=" + lat + "&lon=" + lon + "&speed=" + speed +
            "&accuracy=" + accuracy + "&altitude=" + altitude +  "&heading=" + heading + "&activity=" + activity;

        fetch(URL)
        // TODO: don't actually need a response
            .then((response) => response.json())
            .then((responseData) => {
            })
            .catch((error) => {
                alert("Something wrong with fetch gnss")
            })
            .done();
    }

    fetchAccelerometer(x, y, z, activity) {


        var URL = "http://188.166.168.99.5000:5000/storeACCELEROMETER?&x=" + x + "&y=" + y +
            "&z=" + z + "&activity=" + activity;

        fetch(URL)
        // TODO: don't actually need a response
            .then((response) => response.json())
            .then((responseData) => {
            })
            .catch((error) => {
                alert("Something wrong with fetch accelerometer")
            })
            .done();
    }



    // shouldComponentUpdate(){
    //     // return true;
    //     return !this.textInput.isFocused();
    // }

    textInput = (text) => {
        this.setState((state) =>{
            return {
                activity: text

            };
        });
    };

    render(){
        // TODO: if prevLocation =! New location then this.fetchGeolocation
        // this.fetchGeolocation(this.state.lat,this.state.lon,this.state.speed,this.state.accuracy, this.state.altitude, this.state.heading, this.state.activity);
        this.fetchAccelerometer(this.state.x, this.state.y, this.state.z, this.state.activity);
        return (
            <View>
              <Text>
                <Text style={styles.title}>Lat: </Text> {this.state.lat}
                <Text style={styles.title}>Lon: </Text> {this.state.lon}
                <Text style={styles.title}>Speed: </Text> {this.state.speed}
                <Text style={styles.title}>Accuracy: </Text> {this.state.accuracy}
                <Text style={styles.title}>Altitude: </Text> {this.state.altitude}
                <Text style={styles.title}>X: </Text> {this.state.x}
                <Text style={styles.title}>Y: </Text> {this.state.y}
                <Text style={styles.title}>Z: </Text> {this.state.z}

                <Text style={styles.title}>Activity: </Text> {this.state.activity}
              </Text>

            <TextInput

                style={{height: 40, borderColor: 'gray', borderWidth: 1}}
                onSubmitEditing={(activity) => this.textInput(activity.nativeEvent.text)}
            />
            </View>
        )
    }
}
const styles = StyleSheet.create({
    title: {
        fontWeight: '500',
    },
});

AppRegistry.registerComponent('masApp', () => masApp);
