import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Button, View, TextInput, Alert, Text } from 'react-native';
import React from 'react';
import axios from 'axios';
import TopBar from './TopBar';


export default function App() {
  const [message, onChangeMessage] = React.useState();
  const [words, setWords] = React.useState([])
  const [urls, setUrls] = React.useState([])
  const [isSmish, setIsSmish] = React.useState(null)
  const onSumitMessage = () =>{
    if(message.length === 0){
      setWords([])
      setUrls([])
      setIsSmish(null)
    }else{
    axios.get('http://34.227.27.166:8000/app/Analyze_Text?text='+message).then(response=>{
       console.log(response.data)
      if(response.data.result === "ham"){
        Alert.alert("Smish is not Detected")
        setIsSmish(false)
      }else{
        setWords(response.data.data.words)
        setUrls(response.data.data.urlResult)
        setIsSmish(true)
        Alert.alert("Smish Detected")
      }
    })}
    
  }
  
  return (
    <View style={styles.container}>
      <TopBar/>
      <View style={styles.internalcontainer}>
      {isSmish !== null && isSmish && <Text style={styles.unSafeText}>Message is Unsafe</Text>}
      {isSmish !== null && !isSmish && <Text style={styles.safeText}>Message is Safe</Text>}
      {words.length !== 0 && <Text style={styles.allText}>{message.split(" ").map((m,id)=>{
        let word = m.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"")
        if(words.includes(word.toLowerCase())){
          if(word.length === m.length)
            return <Text style={styles.innerText}>{m + " "}</Text>
          else{
            let diff = m.length - word.length
            let punctuation = m.slice(-diff)
            return <><Text style={styles.innerText}>{word}</Text><Text>{punctuation+ " "}</Text></>
          }
          
        }
        for(let i =0; i<urls.length;i++){
          if(urls[i].url === m){
            if(urls[i].result === "smish"){
                return <Text style={styles.innerText}>{m + " "}</Text>
            }else{
              return <Text>{m + " "}</Text>
            }
          }
        }
        return <Text>{m + " "}</Text>
      })}</Text>}
      <TextInput  value={message} onChangeText={onChangeMessage} style={styles.input}/>
      <Button onPress={onSumitMessage} title="Check Message"/>
      <StatusBar style="auto" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    paddingTop: 80
  
  },
  internalcontainer:{
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    padding: 12,
    paddingTop: 40
  },
  input: {
    height: 90,
    margin: 12,
    borderWidth: 1,
    padding: 10,
    width: 300
  },
  innerText: {
    color: 'red',
    fontWeight: 'bold'
  },
  allText:{
    fontSize:20,
    marginBottom: 100
  },
  unSafeText:{
    color: 'red',
    fontSize: 30,
    fontWeight:"bold",
    marginBottom: 30
  },
  safeText:{
    color: 'green',
    fontSize:30,
    fontWeight:"bold",
    marginBottom: 30
  }
});
