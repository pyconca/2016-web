import Analyzer from './data/analyzer.jsx';

let scheduleData = require('../../../../data/schedule.json').days;
let roomData     = require('../../../../data/schedule.json').rooms;
let talkData     = require('./talks.json');
let analyzer     = new Analyzer();
let days         = analyzer.objectifySessions(scheduleData, talkData);
let timeline     = analyzer.analyzeTimeline(days);

import React              from 'react';
import ReactDOM, {render} from 'react-dom';
import Core               from './com/core.jsx';

for (let dom of document.querySelectorAll('.widget-schedule')) {
    ReactDOM.render(<Core timeline={ timeline } rooms={ roomData } />, dom);
}
