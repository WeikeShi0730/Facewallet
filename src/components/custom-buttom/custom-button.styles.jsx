import styled from "styled-components";

export const CustomButtonContainer = styled.button`
  min-width: 165px;
  width: auto;
  height: 50px;
  letter-spacing: 0.5px;
  line-height: 50px;
  padding: 0 35px 0 35px;
  font-size: 12px;
  background-color: black;
  color: white;
  text-transform: uppercase;
  font-family: "formula1-display-regular";
  font-weight: bolder;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
  @media screen and (max-width: 1200px) {
    font-size: 10px;
  }
`;
