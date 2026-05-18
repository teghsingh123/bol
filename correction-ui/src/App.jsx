import { use, useRef, useState } from "react";

function App() {
  const [isPLaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [lyrics, setLyrics] = useState([]);

  const audioRef = useRef(null);

  //file input that reads the txt file and calls parseLyrics

  function handleFileUpload(e) {
    const file = e.target.files[0];
    const reader = new FileReader()
    reader.onload = e => {
      const text = e.target.result;
      const parsed = parseLyrics(text);
      console.log(parsed);
      setLyrics(parsed);
    }
    console.log(e.target.files);
    reader.readAsText(file);

    //handleFileUpload does not need to return anything
    //its simply an event handler
    //It reads the file and sets state thats it
  }

  function handleAudioUpload(e) {
    const file = e.target.files[0];
    //takes file from computer and creates a temporary url the browser can use to access it
    //normally a browser can only load audio from a web url (i.e .com/test.mp3)
    //createObjectURL will bridge that gap
    const url = URL.createObjectURL(file);
    audioRef.current.src = url;
  }

  //given a time, find which lyric it falls under to highlight that line
  //start from the end to find the last line whose start is less than or equal to currentTime
  function findCurrentLine(lyrics, currentTime) {
    for (let i = lyrics.length - 1; i >= 0; i--) {
      if (currentTime >= lyrics[i].start) {
        //return the index not the line because we can do more with it
        //ex: highlight that specific line, scroll to that position, access both index and line content
        return i;
      }
    }
    //if nothing matches return default to the first line
    return 0;
  }

  const activeLine = findCurrentLine(lyrics, currentTime);
  return (
    <div>
      <h1>Bol - Correction UI</h1>
      <input type="file" accept=".txt" onChange={handleFileUpload}/>
      <input type="file" accept=".mp3" onChange={handleAudioUpload} />
      <audio ref={audioRef} controls onTimeUpdate={() => setCurrentTime(audioRef.current.currentTime)} />
      {/* Loop through lyrics array and render a div for each line. Use key=index to assign a unique key to each item in the list. */}
      {lyrics.map((line, index) => (
        //if the line is active, double the font size and set opacity to 1
        <div key={index} style={{fontSize : index === activeLine ? "2rem" : "1rem", opacity : index === activeLine ? 1 : 0.4}}>
          {line.text}
        </div>
      ))}
    </div>
  )
}


// Parse through the lyrics to separate the timestamps from the actual lyrics and convert the timestamps into only seconds
function parseLyrics(text) {
  const lines = text.split("\n");// split the lyrics line by line

  return lines
    .filter(line => line.trim() !== "")
    .map(line => { // for every line map the line to the function
      const [timestamp, lyrics] = line.split("] "); // split at the ] to separate the timestamp at the beginning from the line
      const [minutes, seconds] = timestamp.replace("[", "").split(":");

      return {
        start: parseInt(minutes) * 60 + parseInt(seconds),
        text: lyrics
      }
    })
}

export default App