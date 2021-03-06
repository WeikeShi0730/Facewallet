import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
body {
    font-family: "formula1-display-regular";

    @media screen and (max-width: 1200px) {
        padding: 10px;
    }
  }
  
  a {
    text-decoration: none;
    color: balck;
  }
  
  * {
    box-sizing: border-box;
  }
  

`;
