import React, { useState } from "react";

import Spinner from "../spinner/spinner.component";

function WithSpinner(WrappedComponent) {
  function HOC(props) {
    const [isLoading, setIsLoading] = useState(false);

    const setLoading = (isComponentLoading) => {
      setIsLoading(isComponentLoading);
    };

    return isLoading ? (
      <div>
        <Spinner />
      </div>
    ) : (
      <WrappedComponent setIsLoading={setLoading} {...props} />
    );
  }

  return HOC;
}

export default WithSpinner;
