import React, { forwardRef } from "react";
import Webcam from "react-webcam";

import { CheckoutPageContainer } from "./camera-window.styles";

const WebcamWindow = forwardRef((props, ref) => {
  const videoConstraints = {
    width: 400,
    height: 400,
    facingMode: "user",
  };

  return (
    <CheckoutPageContainer>
      <Webcam
        ref={ref}
        audio={false}
        videoConstraints={videoConstraints}
        width={400}
        height={400}
        mirrored={true}
        screenshotFormat="image/jpeg"
      />
    </CheckoutPageContainer>
  );
});

export default WebcamWindow;
