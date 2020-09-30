import React from "react";
import Webcam from "react-webcam";

import { CheckoutPageContainer } from "./camera-window.styles";

function WebcamWindow() {
  const videoConstraints = {
    width: 500,
    height: 500,
    facingMode: "user",
  };

  return (
    <CheckoutPageContainer>
      <Webcam
        audio={false}
        videoConstraints={videoConstraints}
        width={500}
        height={500}
        mirrored={true}
        screenshotFormat="image/jpeg"
      />
    </CheckoutPageContainer>
  );
}

export default WebcamWindow;
