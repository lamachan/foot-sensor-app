/* eslint no-magic-numbers: 0 */
import React, { useState } from 'react';

import { FeetSensors } from '../lib';

const App = () => {

    const [state, setState] = useState({L0:0, L1:0, L2:0, R0:0, R1:0, R2:0});
    const setProps = (newProps) => {
            setState(newProps);
        };

    return (
        <div>
            <FeetSensors
                setProps={setProps}
                {...state}
            />
        </div>
    )
};


export default App;
