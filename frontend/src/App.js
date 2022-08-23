import React, { useRef, useEffect, useState } from "react";
import WebViewer from "@pdftron/webviewer";
import Spinner from "../src/Spinner"
import "./App.css";

const App = () => {
  const [file, setFile] = useState("PDFTRON_about.pdf");
  const [IsFileConvert,setIsFileConvert] = useState(false);
  const inputRef = useRef(null);

  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  const handleClick = () => {
    // 👇️ open file input box on click of other element
    inputRef.current.click();
  };
  const handleFileChange = (event) => {
    console.log("event.target.files[0]", event.target.files[0].name);
    const fileObj = event.target.files && event.target.files[0];
    if (!fileObj) {
      return;
    }
    setFile(event.target.files[0].name);
    // setIsFileConvert (true)
    // console.log("fileObj is", fileObj);
    // let url = "";
    // const response = await fetch(url, {
    //     method: 'POST',
    //     body: formData,
    //     Headers: {
    //           'Accept': 'application.json',
    //           'Content-Type': 'application/json'
    //         },
    // }
    // .then(function(response){ 
      
    //   setFile("21000795-HD-10157.pdf");
    //   console.log(response)
    //   FileUpload(response.data)
    // setIsFileConvert (false)
    //   // return response.json()
    // })
    // .catch((error) =>
    // {
      // setIsFileConvert (false)
    //   console.log(error)
    // })
    // );
    // setFile(event.target.files[0].name);
    // 👇️ reset file input
    // event.target.value = null;

    // 👇️ is now empty
    // console.log(event.target.files);

    // // 👇️ can still access file object here
    // console.log(fileObj);
    // console.log(fileObj.name);
  };

  const viewer = useRef(null);

  // if using a class, equivalent of componentDidMount
  useEffect(() => {
    WebViewer(
      {
        path: "/webviewer/lib",
        initialDoc: "/files/" + file, //"/files/21000795-HD-10157.pdf", // "/files/PDFTRON_about.pdf",
      },
      viewer.current
    ).then((instance) => {
      const { documentViewer, annotationManager, Annotations } = instance.Core;

      documentViewer.addEventListener("documentLoaded", () => {
        const rectangleAnnot = new Annotations.RectangleAnnotation({
          PageNumber: 1,
          // values are in page coordinates with (0, 0) in the top left
          X: 100,
          Y: 150,
          Width: 200,
          Height: 50,
          Author: annotationManager.getCurrentUser(),
        });

        annotationManager.addAnnotation(rectangleAnnot);
        // need to draw the annotation otherwise it won't show up until the page is refreshed
        annotationManager.redrawAnnotation(rectangleAnnot);
      });
    });
  });

  // const FileUpload = async(props) =>
  // {
  //   const { filePath = ""} = props
  //   return  WebViewer(
  //     {
  //       path: "/webviewer/lib",
  //       initialDoc: filePath, //"/files/21000795-HD-10157.pdf", // "/files/PDFTRON_about.pdf",
  //     },
  //     viewer.current
  //   ).then((instance) => {
  //     const { documentViewer, annotationManager, Annotations } = instance.Core;

  //     documentViewer.addEventListener("documentLoaded", () => {
  //       const rectangleAnnot = new Annotations.RectangleAnnotation({
  //         PageNumber: 1,
  //         // values are in page coordinates with (0, 0) in the top left
  //         X: 100,
  //         Y: 150,
  //         Width: 200,
  //         Height: 50,
  //         Author: annotationManager.getCurrentUser(),
  //       });

  //       annotationManager.addAnnotation(rectangleAnnot);
  //       // need to draw the annotation otherwise it won't show up until the page is refreshed
  //       annotationManager.redrawAnnotation(rectangleAnnot);
  //     });
  //   });
  // }

  return (
    <div className="App">
      <div className="header">React sample</div>
      <button>OPEN</button>
      {IsFileConvert ? <Spinner />:<div className="webviewer" ref={viewer}></div>}

      <input
        style={{ display: "none" }}
        ref={inputRef}
        type="file"
        onChange={handleFileChange}
      />

      <button onClick={handleClick}>Convert to word</button>
    </div>
  );
};

export default App;

