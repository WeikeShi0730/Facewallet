import styled from "styled-components";
import { Link } from "react-router-dom";

export const HeaderContainer = styled.div`
  text-align: centre;
`;

export const OptionLink = styled(Link)`
  padding: 10px 15px;
  cursor: pointer;
  @media screen and (max-width: 1200px) {
    padding: 5px;
  }
`;