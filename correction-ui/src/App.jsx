import { use, useEffect, useRef, useState } from "react";

function App() {
  const [isPLaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [lyrics, setLyrics] = useState([]);
  const [editingIndex, setEditingIndex] = useState(null); //null = read mode, some number = write mode for that line
  const [editText, setEditText] = useState(""); //text to be edited

  const audioRef = useRef(null);
  const lineRefs = useRef([]) //array of refs for each lyric line, used to scroll the active line into view
  


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


  //Checks if editText is different from original
  //If yes, updates lyrics array
  //Sets editingIndex back to null
  function saveEdit(index) {
    if (editText !== lyrics[index].text) {
      const updated = [...lyrics]; // we cannot mutate state directly, so we have to create a new array and use setLyrics
      updated[index] = {...lyrics[index], text: editText}; //copies all properties of current line and then overrides text property with new edited value
      setLyrics(updated);
    }
    setEditingIndex(null);
  }




  const activeLine = findCurrentLine(lyrics, currentTime);


  //smooth scrolling
  //puts the active line at the center of the screen by using scrollIntoView
  useEffect(() => {
    lineRefs.current[activeLine]?.scrollIntoView({behavior: "smooth", block: "center"}); 
  }, [activeLine]); //does every time activeLine changes

  return (
    <div>
      <h1>Bol - Correction UI</h1>
      <input type="file" accept=".txt" onChange={handleFileUpload}/>
      <input type="file" accept=".mp3" onChange={handleAudioUpload} />
      <audio ref={audioRef} controls onTimeUpdate={() => setCurrentTime(audioRef.current.currentTime)} />
      {/* Loop through lyrics array and render a div for each line. Use key=index to assign a unique key to each item in the list. */}
      {lyrics.map((line, index) => (
        //if the line is active, double the font size and set opacity to 1
        <div 
          key={index}
          ref={el => lineRefs.current[index] = el}
          style={{
            fontSize : index === activeLine ? "2rem" : "1rem", 
            opacity : index === activeLine ? 1 : 0.4,
            margin: "1rem 0",
            lineHeight: 1.5
            }}>
          {/* Check if the line is the one being edited. If yes, show the input field.
              If not, show the span. Clicking it sets editingIndex to this line's index
              and editText to the current text, and switches to edit mode.
          */}
          {index === editingIndex
            ? <input 
                value={editText} 
                onChange={e => setEditText(e.target.value)} 
                style={{fontSize: "inherit", width: "100%", textAlign: "center"}}
                onBlur={() => saveEdit(index)}
                onKeyDown={e => {if (e.key === "Enter") saveEdit(index) }}
                />
            : <span onClick={() => {
                setEditingIndex(index);
                setEditText(line.text);}}>
                {line.text}
              </span>}
        </div>
      ))}
      <button onClick={() => exportLyrics(lyrics)}> Export Lyrics</button>
    </div>
  )
}


// Parse through the lyrics to separate the timestamps from the actual lyrics and convert the timestamps into only seconds
function parseLyrics(text) {
  const lines = text.split("\n");// split the lyrics line by line

  return lines
    .filter(line => line.trim() !== "") //get rid of the last line which had timestamp NaN
    .map(line => { // for every line map the line to the function
      const [timestamp, lyrics] = line.split("] "); // split at the ] to separate the timestamp at the beginning from the line
      const [minutes, seconds] = timestamp.replace("[", "").split(":");

      return {
        start: parseInt(minutes) * 60 + parseInt(seconds),
        text: lyrics
      }
    })
}

//Export the corrected lyrics back to a txt file

function exportLyrics(lyrics) {
  
  //convert start back to minutes and seconds
  const text = lyrics.map(line => {
    const minutes = Math.floor(line.start / 60);
    const seconds = line.start % 60;

    //create string in original txt format
    const str = "[" + String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0") + "] " + line.text;
    return str
  }).join("\n"); //join by new line.

  //create the txt file using Blob
  const blob = new Blob([text], {type: "text/plain"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "corrected_lyrics.txt";
  a.click();
  URL.revokeObjectURL(url);

}

export default App