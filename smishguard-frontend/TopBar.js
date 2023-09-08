import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default class TopBar extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <Text></Text>
        <Text style={styles.topBarText}>SmishGuard</Text>
        <Text></Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    alignSelf: 'stretch',
    height: 52,
    flexDirection: 'row', // row
    backgroundColor: '#ffff99',
    alignItems: 'center',
    justifyContent: 'space-between', // center, space-around
    paddingLeft: 10,
    paddingRight: 10,
    
  },
  topBarText:{
    fontSize: 25,
    fontWeight:"bold"
  }
});
