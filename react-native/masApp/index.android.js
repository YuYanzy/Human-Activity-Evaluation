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

            },
            (error) => alert(JSON.stringify(error)),
            {enableHighAccuracy: true, timeout: 20000, maximumAge: 0, setInterval: 50000}
            //FIXME: setintervall?
        );

        SensorManager.startAccelerometer(100); // Start the accelerometer with a minimum delay of 100 ms between events
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



        SensorManager.startGyroscope(100);
        DeviceEventEmitter.addListener("Gyroscope", function (data) {
            var xg = data.x;
            var yg = data.y;
            var zg= data.z;

            this.setState({
                xg: xg,
                yg: yg,
                zg: zg
            });
        }.bind(this));

        SensorManager.startOrientation(100);
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

        SensorManager.startStepCounter(1000);
        DeviceEventEmitter.addListener('StepCounter', function (data) {
            var steps = data.steps;

            this.setState({
                steps: steps
            });
        }.bind(this));

    //     //TODO maybe this wil work better?
    }



    fetchData(lat, lon, speed, accuracy, altitude, heading, x, y, z) {


        // var URL = "http://10.243.0.214:5000/store?lat=" + lat + "&lon=" + lon + "&speed=" + speed + "&accuracy=" + accuracy + "&altitude=" + altitude + "&altitudeAccuracy=" + altitudeAccuracy + "&heading=" + heading + "&x=" + x + "&y=" + y + "&z=" + z;
        var URL = "http://10.243.0.232:5000/store?lat=" + lat + "&lon=" + lon + "&speed=" + speed + "&accuracy=" + accuracy + "&altitude=" + altitude +  "&heading=" + heading + "&x=" + x + "&y=" + y + "&z=" + z;

        fetch(URL)
        // TODO: don't actually need a response
            .then((response) => response.json())
            .then((responseData) => {
            })
            .catch((error) => {
                alert("Something wrong with fetch")
            })
            .done();
    }

    fetchText(activity) {
        var URL = "http://10.243.0.232:5000/test?activity=" + activity;

        fetch(URL)
        // TODO: don't actually need a response
            .then((response) => response.json())
            .then((responseData) => {
            })
            .catch((error) => {
                alert("Something wrong with fetch2")
            })
            .done();
    }


    // shouldComponentUpdate(){
    //     // return true;
    //     return !this.textInput.isFocused();
    // }

    textInput = (text) => {
        // this.setState({activity:activity});
        this.setState((state) =>{
            return {
                activity: text

            };
        });
    };

    render(){
        this.fetchData(this.state.lat,this.state.lon,this.state.speed,this.state.accuracy, this.state.altitude, this.state.heading, this.state.x, this.state.y, this.state.z);
        this.fetchText(this.state.activity);

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
                <Text style={styles.title}>XG: </Text> {this.state.xg}
                <Text style={styles.title}>YG: </Text> {this.state.yg}
                <Text style={styles.title}>ZG: </Text> {this.state.zg}
                <Text style={styles.title}>Azimuth: </Text> {this.state.azimuth}
                <Text style={styles.title}>Pitch: </Text> {this.state.pitch}
                <Text style={styles.title}>Roll: </Text> {this.state.roll}
                <Text style={styles.title}>Steps: </Text> {this.state.steps}
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
