import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
// import Feet from '../../../public/assets/feet.svg'
// import Cat from '../../../assets/cat.jpg'

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
            <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
            width="1079.000000pt" height="1280.000000pt" viewBox="0 0 1079.000000 1280.000000"
            preserveAspectRatio="xMidYMid meet">
            <g transform="translate(0.000000,1280.000000) scale(0.100000,-0.100000)"
            fill="#000000" stroke="none">
            <path d="M3825 12772 c-99 -33 -164 -74 -238 -149 -76 -78 -101 -113 -151
            -213 -77 -153 -113 -294 -123 -480 -9 -188 18 -347 87 -495 89 -193 222 -308
            408 -356 200 -51 397 5 547 156 154 156 225 358 225 644 0 273 -67 494 -206
            677 -87 115 -184 183 -320 223 -92 27 -131 26 -229 -7z"/>
            <path d="M6725 12776 c-87 -28 -136 -54 -200 -105 -145 -117 -258 -332 -300
            -569 -22 -125 -20 -343 4 -460 51 -246 171 -422 352 -517 246 -129 554 -58
            725 168 124 163 184 387 171 637 -10 193 -46 331 -131 494 -92 178 -231 302
            -391 351 -98 30 -139 30 -230 1z"/>
            <path d="M2508 12287 c-113 -32 -218 -124 -282 -247 -47 -90 -66 -159 -72
            -270 -14 -231 91 -443 261 -526 54 -26 70 -29 155 -29 85 0 101 3 155 29 206
            101 329 383 281 644 -42 234 -197 396 -391 408 -33 2 -81 -2 -107 -9z"/>
            <path d="M8099 12287 c-140 -40 -259 -175 -305 -347 -23 -85 -23 -243 -1 -330
            42 -162 147 -303 272 -365 54 -26 70 -29 155 -30 85 0 101 3 155 29 365 179
            344 840 -32 1018 -73 35 -173 45 -244 25z"/>
            <path d="M1562 11693 c-58 -20 -152 -109 -185 -175 -152 -304 17 -697 291
            -676 106 8 196 74 254 185 45 86 62 157 62 258 -1 141 -50 262 -141 345 -83
            76 -182 98 -281 63z"/>
            <path d="M9061 11699 c-107 -31 -199 -141 -237 -282 -18 -69 -18 -208 1 -282
            75 -284 350 -388 527 -198 85 91 118 186 118 334 0 120 -24 204 -83 290 -83
            121 -204 173 -326 138z"/>
            <path d="M799 11057 c-203 -76 -240 -405 -68 -601 172 -195 417 -107 454 164
            15 111 -40 276 -120 356 -79 79 -185 111 -266 81z"/>
            <path d="M9875 11061 c-119 -30 -223 -148 -255 -292 -18 -83 -9 -213 19 -269
            88 -174 270 -202 408 -64 188 188 152 556 -60 619 -55 16 -66 17 -112 6z"/>
            <path d="M3097 10839 c-689 -57 -1449 -415 -2192 -1032 -652 -543 -908 -1136
            -830 -1927 42 -425 132 -744 533 -1895 235 -673 309 -915 417 -1360 154 -631
            259 -1178 324 -1685 53 -414 64 -662 40 -890 -7 -63 -13 -200 -13 -305 0 -218
            16 -312 85 -520 201 -605 726 -1069 1339 -1184 295 -55 325 -55 605 1 490 97
            940 450 1177 921 147 294 206 557 194 872 -14 403 -147 743 -443 1136 -127
            168 -238 293 -567 639 -296 310 -346 364 -467 505 -314 365 -523 706 -631
            1027 -124 372 -138 726 -42 1048 36 120 132 309 210 414 139 187 292 327 641
            588 234 175 377 299 499 434 330 365 579 768 714 1161 176 508 171 973 -15
            1337 -264 518 -834 777 -1578 715z"/>
            <path d="M7264 10839 c-358 -32 -679 -169 -905 -386 -416 -401 -501 -1020
            -237 -1728 136 -366 387 -764 692 -1099 124 -136 268 -262 500 -435 260 -194
            365 -281 482 -403 379 -392 507 -858 389 -1414 -86 -408 -308 -810 -694 -1259
            -121 -141 -171 -195 -467 -505 -329 -346 -440 -471 -567 -639 -296 -393 -429
            -733 -443 -1136 -12 -312 47 -578 191 -865 240 -479 687 -830 1180 -928 280
            -56 310 -56 605 -1 612 115 1138 580 1339 1184 68 205 84 303 85 515 0 102 -5
            241 -13 310 -24 238 -14 468 40 890 69 537 186 1138 350 1795 92 367 174 627
            429 1360 256 737 346 1020 415 1309 170 714 107 1308 -190 1781 -174 278 -414
            521 -800 812 -824 620 -1639 908 -2381 842z"/>
            <path d="M178 10480 c-69 -21 -120 -86 -153 -196 -30 -98 -31 -122 -4 -221 31
            -113 66 -178 125 -232 239 -218 476 135 318 474 -62 134 -181 207 -286 175z"/>
            <path d="M10474 10467 c-117 -56 -197 -216 -197 -392 0 -208 126 -348 273
            -304 57 17 140 94 172 161 31 63 68 195 68 241 0 47 -44 183 -74 225 -59 85
            -152 111 -242 69z"/>
            </g>
            </svg>
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