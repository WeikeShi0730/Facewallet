import React, { forwardRef } from "react";
import Webcam from "react-webcam";

import "./camera-window.styles.scss";

const WebcamWindow = forwardRef((props, ref) => {
  const videoConstraints = {
    width: 400,
    height: 400,
    facingMode: "user",
  };

  return (
    <Webcam
    className="webcam"
      ref={ref}
      audio={false}
      videoConstraints={videoConstraints}
      width={400}
      height={400}
      mirrored={true}
      screenshotFormat="image/jpeg"
    />
  );
});

export default WebcamWindow;
