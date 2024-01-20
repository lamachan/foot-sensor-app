import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

// Function to calculate circle size based on value
const calculateCircleSize = value => {
    // Define a base size for the circle
    const baseSize = 30;
  
    // Adjust the size based on the value
    return baseSize + value * 0.03; // Modify this multiplier as needed
  };
  
  // Styled component for a dynamically sized circle
const Circle = styled.div`
  border-radius: 50%;
  background-color: ${({ isAnomaly }) => (isAnomaly ? 'red' : 'blue')}; /* Set background color based on anomaly prop */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 5px;
  width: ${({ value }) => calculateCircleSize(value)}px;
  height: ${({ value }) => calculateCircleSize(value)}px;
`;

const Value = styled.p`
  font-size: 16px;
  font-weight: bold;
  color: white;
`;

const FeetSensors = (props) => {
    const {id, L0, L1, L2, R0, R1, R2, anomaly_L0, anomaly_L1, anomaly_L2, anomaly_R0, anomaly_R1, anomaly_R2} = props;

    return (
        <div id={id}>
            <Circle value={L0} isAnomaly={anomaly_L0}>
                <Value>{L0}</Value>
            </Circle>
            <Circle value={L1} isAnomaly={anomaly_L1}>
                <Value>{L1}</Value>
            </Circle>
            <Circle value={L2} isAnomaly={anomaly_L2}>
                <Value>{L2}</Value>
            </Circle>
            <Circle value={R0} isAnomaly={anomaly_R0}>
                <Value>{R0}</Value>
            </Circle>
            <Circle value={R1} isAnomaly={anomaly_R1}>
                <Value>{R1}</Value>
            </Circle>
            <Circle value={R2} isAnomaly={anomaly_R2}>
                <Value>{R2}</Value>
            </Circle>
        </div>
    );
}

FeetSensors.defaultProps = {};

FeetSensors.propTypes = {
    id: PropTypes.string,
    
    L0: PropTypes.number.isRequired,
    L1: PropTypes.number.isRequired,
    L2: PropTypes.number.isRequired,
    R0: PropTypes.number.isRequired,
    R1: PropTypes.number.isRequired,
    R2: PropTypes.number.isRequired,

    anomaly_L0: PropTypes.bool.isRequired,
    anomaly_L1: PropTypes.bool.isRequired,
    anomaly_L2: PropTypes.bool.isRequired,
    anomaly_R0: PropTypes.bool.isRequired,
    anomaly_R1: PropTypes.bool.isRequired,
    anomaly_R2: PropTypes.bool.isRequired,
    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default FeetSensors;