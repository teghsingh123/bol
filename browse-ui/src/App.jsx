import { useState, useEffect } from "react";

function App() {
  const [albums, setAlbums] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [tracks, setTracks] = useState([]);

  //go to previous album
  function handlePrev() {
    if (currentIndex > 0) setCurrentIndex(currentIndex - 1)
  }

  //go to next album
  function handleNext() {
    if (currentIndex < albums.length - 1) setCurrentIndex(currentIndex + 1)
  }


  //fetch tracks for an album from the api
  function handleAlbumClick(id) {
    setSelectedAlbum(id);
    fetch(`http://127.0.0.1:5000/albums/${id}/tracks`)
      .then(res => res.json())
      .then(data => setTracks(data))
  }

  //fetch albums from api
  useEffect(() => {
    fetch("http://127.0.0.1:5000/albums") //make the fetch request
      .then(res => res.json()) // when the response arrives, parse it as JSON
      .then(data => setAlbums(data)); // when that's done, set the album's state
  }, [])

  

  return (
    <div>
      <h1>Bol</h1>
      <div style={{ display: "flex", alignItems: "center", gap: "2rem", justifyContent: "center"}}>
        <button onClick={() => handlePrev() }> Previous Album</button>
        {albums[currentIndex] && (
        <div style={{ display: "flex", gap: "2rem"}}>
          {/* Left side - album info */}
          <div style={{ flex: 1 }} onClick={() => handleAlbumClick(albums[currentIndex].id)}>
            <h2>{albums[currentIndex].title}</h2>
            <p>{albums[currentIndex].artist}</p>
            <p>{albums[currentIndex].year}</p>
          </div>
          <div style={{ flex: 1}}>
            {tracks.map((track, index) => (
              <div key={index}>{track.title}</div>
            ))}
          </div>
        </div>
      )}

        <button onClick={() => handleNext() }> Next Album</button>
      </div>
      <div style={{ display: "flex", gap: "0.5rem", justifyContent: "center", marginTop: "1rem"}}>
        {albums.map((album,index) => (
        <div key={index} style={{
          width: "10px",
          height: "10px",
          borderRadius: "50%",
          backgroundColor: index === currentIndex ? "black" : "gray"
          }}>
        </div>
      ))}
      </div>


    </div>
  )
}

export default App